"""Organizer workflows use synthetic data and never contact delivery providers."""
import json
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from django.contrib.auth.models import Permission
from django.contrib.admin.models import LogEntry
from django.db import close_old_connections
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from rest_framework.test import APIClient
from apps.users.models import User
from apps.games.models import Game, Group, Character, Question, Answer, Application, Tag
from apps.games.organizer_content import revision
from apps.notifications.models import Mailing, Notification


class ContentFixtures:
    def setUp(self):
        self.staff = User.objects.create_superuser('organizer', 'staff@example.invalid', 'synthetic')
        self.game = Game.objects.create(title='Synthetic game', alias='synthetic', price=1000, open_applications=True)
        self.other = Game.objects.create(title='Other game', alias='other')
        self.group = Group.objects.create(game=self.game, name='Faction')
        self.family = Group.objects.create(game=self.game, name='Family', family=True)
        self.foreign = Group.objects.create(game=self.other, name='Other faction')
        self.character = Character.objects.create(name='Character', alias='character', group=self.group)
        self.player = User.objects.create_user('player', 'player@example.invalid', telegram_chat_id='synthetic-chat')
        self.app = Application.objects.create(game=self.game, user=self.player)
        self.client = APIClient(); self.client.force_authenticate(self.staff)
        self.base = f'/api/organizer/games/{self.game.pk}/'

    def patch(self, resource, instance, **fields):
        instance.refresh_from_db()
        return self.client.patch(f'{self.base}{resource}/{instance.pk}/',
            {'expected_revision': revision(instance), **fields}, format='json')

    def delete(self, resource, instance):
        return self.client.delete(f'{self.base}{resource}/{instance.pk}/', {'expected_revision': revision(instance)}, format='json')

    def draft(self, applications=None):
        response = self.client.post(self.base+'mailings/', {'text':'<p>Hello <strong>player</strong></p>',
            'time':timezone.now().isoformat(), 'applications': applications or []}, format='json')
        self.assertEqual(response.status_code,201,response.data)
        return response.data['id']

    def preview(self, pk):
        return self.client.get(f'{self.base}mailings/{pk}/preview/').data

    def confirm(self, pk, snapshot, key=None):
        return self.client.post(f'{self.base}mailings/{pk}/confirm/',
            {'audience_revision':snapshot['audience_revision'],'idempotency_key':str(key or uuid4())},format='json')


class OrganizerContentTests(ContentFixtures, TestCase):
    def test_permissions_for_every_resource(self):
        resources=['groups','characters','tags','questions','applications','mailings']
        for user in [None,self.player,User.objects.create_user('limited',is_staff=True)]:
            self.client.force_authenticate(user)
            for resource in resources:
                with self.subTest(resource=resource,user=user):
                    self.assertIn(self.client.get(self.base+resource+'/').status_code,[401,403])
        reader=User.objects.create_user('reader','reader@example.invalid',is_staff=True)
        reader.user_permissions.add(Permission.objects.get(codename='view_group',content_type__app_label='games'))
        self.client.force_authenticate(reader)
        self.assertEqual(self.client.get(self.base+'groups/').status_code,200)
        self.assertEqual(self.patch('groups',self.group,name='Forbidden').status_code,403)
        self.assertEqual(self.delete('groups',self.group).status_code,403)

    def test_organizer_reads_do_not_consume_write_quota(self):
        from rest_framework.test import APIRequestFactory
        from apps.games.organizer_content import OrganizerGroupViewSet
        view=OrganizerGroupViewSet();view.request=APIRequestFactory().get('/')
        self.assertEqual(view.get_throttles(),[])
        view.request=APIRequestFactory().patch('/')
        self.assertTrue(view.get_throttles())

    def test_groups_create_cycles_scope_and_protected_delete(self):
        result=self.client.post(self.base+'groups/',{'name':'Child','parent':self.group.pk},format='json')
        self.assertEqual(result.status_code,201,result.data)
        child=Group.objects.get(pk=result.data['id'])
        self.assertEqual(child.game,self.game)
        self.assertEqual(self.patch('groups',self.group,parent=child.pk).status_code,400)
        self.assertEqual(self.patch('groups',self.group,parent=self.foreign.pk).status_code,400)
        self.assertEqual(self.patch('groups',self.group,parent=self.family.pk).status_code,400)
        self.assertEqual(self.patch('groups',self.group,family=True).status_code,400)
        self.assertEqual(self.delete('groups',self.group).status_code,400)
        response=self.patch('groups',self.group,hidden=True)
        self.assertEqual(response.status_code,200,response.data)
        self.assertIn(child.pk,response.data['descendants'])
        self.assertEqual(response.data['character_count'],1)
        self.assertEqual(self.client.get(f'{self.base}groups/{self.foreign.pk}/').status_code,404)

    def test_character_complete_save_and_relation_guards(self):
        tag=Tag.objects.create(name='Tag',color='#112233')
        result=self.patch('characters',self.character,name='Changed',name_eng='English',alias='changed',
            description='Description',order=7,family=self.family.pk,master=self.staff.pk,tags=[tag.pk])
        self.assertEqual(result.status_code,200,result.data)
        self.character.refresh_from_db(); self.assertEqual(self.character.name_eng,'English')
        self.assertEqual(list(self.character.tags.all()),[tag])
        self.assertEqual(self.patch('characters',self.character,group=self.foreign.pk).status_code,400)
        self.assertEqual(self.patch('characters',self.character,group=self.family.pk).status_code,400)
        self.assertEqual(self.patch('characters',self.character,group=None,family=None).status_code,400)
        self.app.character=self.character;self.app.save()
        self.assertEqual(self.delete('characters',self.character).status_code,400)
        self.assertEqual(self.delete('tags',tag).status_code,400)

    def test_stale_changes_and_multipart_payload(self):
        old=revision(self.group)
        self.assertEqual(self.patch('groups',self.group,name='New').status_code,200)
        result=self.client.patch(f'{self.base}groups/{self.group.pk}/',{'expected_revision':old,'name':'Stale'},format='json')
        self.assertEqual(result.status_code,409)
        self.group.refresh_from_db()
        result=self.client.patch(f'{self.base}groups/{self.group.pk}/',{'payload':json.dumps({'expected_revision':revision(self.group),'name':'Multipart'})},format='multipart')
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(result['Cache-Control'],'no-store')
        self.assertEqual(self.client.patch(f'{self.base}groups/{self.group.pk}/',{'payload':'[]'},format='multipart').status_code,400)

    def test_shared_tag_requires_acknowledgement(self):
        tag=Tag.objects.create(name='Shared',color='#112233')
        foreign=Character.objects.create(name='Other',alias='other',group=self.foreign);foreign.tags.add(tag)
        self.assertEqual(self.patch('tags',tag,name='Changed').status_code,400)
        self.assertEqual(self.patch('tags',tag,name='Changed',acknowledge_shared=True).status_code,200)

    def test_all_structured_question_types_and_player_roundtrip(self):
        for kind,choices,answer in [('single_choice',['A','B'],'A'),('multiple_choice',['A','B'],['A']),
            ('scale',['1','2'],'2'),('matrix',[['A','B'],['Row']],[['A']]),
            ('matrix_checkbox',[['A','B'],['Row']],[['A','B']])]:
            result=self.client.post(self.base+'questions/',{'title':kind,'type':kind,'choices':choices},format='json')
            self.assertEqual(result.status_code,201,result.data)
            question=Question.objects.get(pk=result.data['id'])
            self.client.force_authenticate(self.player)
            result=self.client.post('/api/applications/apply/',{'game_alias':self.game.alias,f'question_{question.pk}':answer},format='json')
            self.assertEqual(result.status_code,200,result.data)
            self.assertEqual(Answer.objects.get(question=question,application=self.app).value,answer)
            self.client.force_authenticate(self.staff)
            self.assertEqual(self.patch('questions',question,type='line',choices=None).status_code,400)
            self.assertEqual(self.delete('questions',question).status_code,400)
            self.assertEqual(self.patch('questions',question,title='Updated label').status_code,200)

    def test_question_validation_shared_revision_and_removal(self):
        result=self.client.post(self.base+'questions/',{'title':'Bad','type':'matrix','choices':[['A'],[]]},format='json')
        self.assertEqual(result.status_code,400)
        question=Question.objects.create(title='Shared');question.games.set([self.game,self.other])
        self.assertEqual(self.patch('questions',question,title='Changed').status_code,400)
        self.assertEqual(self.patch('questions',question,title='Changed',acknowledge_shared=True).status_code,200)
        self.assertEqual(self.patch('questions',question,games=[self.other.pk],acknowledge_shared=True).status_code,400)
        self.assertEqual(self.delete('questions',question).status_code,400)

    def test_shared_question_keeps_games_with_answers(self):
        question=Question.objects.create(title='Shared');question.games.set([self.game,self.other])
        foreign_app=Application.objects.create(game=self.other,user=self.player)
        Answer.objects.create(question=question,application=foreign_app,value='Existing answer')
        response=self.patch('questions',question,games=[self.game.pk],acknowledge_shared=True)
        self.assertEqual(response.status_code,400)
        self.assertTrue(question.games.filter(pk=self.other.pk).exists())

    def test_delivery_attempts_are_visible_without_provider_exception_text(self):
        from asgiref.sync import async_to_sync
        from bot.database.notifications import mark_notification_failed, mark_notification_sent
        pk=self.draft([self.app.pk]);self.assertEqual(self.confirm(pk,self.preview(pk)).status_code,200)
        notification=Notification.objects.get()
        async_to_sync(mark_notification_failed)(notification.pk,'Forbidden')
        response=self.client.get(f'{self.base}mailings/{pk}/').data['delivery']
        self.assertEqual(response['failed'],1)
        self.assertEqual(response['recipients'][0]['attempts'],1)
        async_to_sync(mark_notification_sent)(notification.pk)
        notification.refresh_from_db()
        self.assertTrue(notification.sent);self.assertEqual(notification.attempts,2)
        self.assertEqual(notification.last_error,'')

    def test_assignment_contribution_and_detail_cooperate(self):
        question=Question.objects.create(title='Question');question.games.add(self.game)
        Answer.objects.create(question=question,application=self.app,value='Answer')
        self.player.likes.add(self.character)
        result=self.patch('applications',self.app,character=self.character.pk,status='confirmed',payed=500,reason='Deposit recorded')
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(result.data['answers'][0]['value'],'Answer')
        self.assertEqual(result.data['likes'],[self.character.pk])
        self.assertEqual(result.data['missing_questions'],[])
        self.assertNotIn('phone',str(result.data))
        self.assertTrue(LogEntry.objects.filter(change_message='Deposit recorded').exists())
        self.assertEqual(self.patch('applications',self.app,payed=600).status_code,400)
        self.assertEqual(self.patch('applications',self.app,payed=-1,reason='Bad').status_code,400)
        other_app=Application.objects.create(game=self.game,user=User.objects.create_user('second'))
        self.assertEqual(self.patch('applications',other_app,character=self.character.pk).status_code,400)
        foreign=Character.objects.create(name='Foreign',alias='foreign',group=self.foreign)
        self.assertEqual(self.patch('applications',other_app,character=foreign.pk).status_code,400)
        self.assertEqual(self.client.get(self.base+'applications/').data[0]['answers'],[])

    def test_mailing_drafts_preview_and_idempotent_confirmation(self):
        pk=self.draft([self.app.pk]);snapshot=self.preview(pk)
        self.assertEqual(Notification.objects.count(),0)
        self.assertEqual(snapshot['eligible'],1)
        key=uuid4();result=self.confirm(pk,snapshot,key)
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(Notification.objects.count(),1)
        self.assertEqual(self.confirm(pk,snapshot,key).status_code,200)
        self.assertEqual(Notification.objects.count(),1)
        self.assertEqual(self.confirm(pk,snapshot).status_code,409)
        mailing=Mailing.objects.get(pk=pk)
        self.assertEqual(self.patch('mailings',mailing,text='Changed').status_code,400)
        self.assertEqual(self.delete('mailings',mailing).status_code,400)

    def test_empty_ineligible_cross_game_and_changed_audiences(self):
        pk=self.draft();self.assertEqual(self.confirm(pk,self.preview(pk)).status_code,400)
        foreign_app=Application.objects.create(game=self.other,user=self.player)
        response=self.client.post(self.base+'mailings/',{'text':'Hello','time':timezone.now().isoformat(),'applications':[foreign_app.pk]},format='json')
        self.assertEqual(response.status_code,400)
        pk=self.draft([self.app.pk]);snapshot=self.preview(pk)
        self.app.status='deleted';self.app.save()
        self.assertEqual(self.confirm(pk,snapshot).status_code,409)
        self.assertEqual(Notification.objects.count(),0)

    def test_html_is_sanitized_and_empty_or_oversized_messages_rejected(self):
        pk=self.draft();mailing=Mailing.objects.get(pk=pk)
        result=self.patch('mailings',mailing,text='<script>bad()</script><p onclick="bad()">Safe</p>')
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(result.data['text'],'<p>Safe</p>')
        for text in ['<p></p>','x'*4097]:
            self.assertEqual(self.patch('mailings',mailing,text=text).status_code,400)


class OrganizerConcurrencyTests(ContentFixtures, TransactionTestCase):
    def test_two_applications_cannot_claim_one_character(self):
        other=Application.objects.create(game=self.game,user=User.objects.create_user('second'))
        barrier=Barrier(2)
        def assign(app):
            close_old_connections()
            try:
                client=APIClient();client.force_authenticate(self.staff)
                version=revision(app);barrier.wait()
                return client.patch(f'{self.base}applications/{app.pk}/',{'expected_revision':version,'character':self.character.pk},format='json').status_code
            finally: close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as pool:
            statuses=list(pool.map(assign,[self.app,other]))
        self.assertEqual(sorted(statuses),[200,400])
        self.assertEqual(Application.objects.filter(character=self.character).count(),1)

    def test_concurrent_confirmation_creates_one_queue(self):
        pk=self.draft([self.app.pk]);snapshot=self.preview(pk);key=str(uuid4());barrier=Barrier(2)
        def confirm(_):
            close_old_connections()
            try:
                client=APIClient();client.force_authenticate(self.staff);barrier.wait()
                return client.post(f'{self.base}mailings/{pk}/confirm/',{'audience_revision':snapshot['audience_revision'],'idempotency_key':key},format='json').status_code
            finally: close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as pool: statuses=list(pool.map(confirm,range(2)))
        self.assertEqual(statuses,[200,200]);self.assertEqual(Notification.objects.count(),1)
