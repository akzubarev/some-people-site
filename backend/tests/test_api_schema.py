"""The documented API uses the same shapes as live serializers."""
from django.test import TestCase
from drf_spectacular.generators import SchemaGenerator
from rest_framework.test import APIClient
from apps.games.models import Answer, Question
from apps.notifications.models import Notification
from apps.users.models import User


class ApiSchemaTests(TestCase):
    def test_schema_is_data_independent_and_separates_private_profiles(self):
        with self.assertNumQueries(0):
            schema = SchemaGenerator().get_schema(request=None, public=True)
        components = schema['components']['schemas']
        self.assertNotIn('phone', components['UserPublic']['properties'])
        self.assertNotIn('email', components['UserPublic']['properties'])
        self.assertIn('phone', components['UserPrivate']['properties'])
        self.assertEqual(components['Group']['properties']['subgroups']['items']['$ref'],
                         '#/components/schemas/Group')
        self.assertEqual(components['UserPrivate']['properties']['likes']['items']['type'], 'integer')
        self.assertTrue(components['Character']['properties']['player']['nullable'])
        paths = schema['paths']
        self.assertEqual(paths['/api/games/characters/']['get']['responses']['200']['content']
            ['application/json']['schema']['items']['$ref'], '#/components/schemas/Character')
        self.assertIn('multipart/form-data', paths['/api/users/update_me/']['put']['requestBody']['content'])
        self.assertIn('201', paths['/api/session/register/']['post']['responses'])
        self.assertEqual(paths['/api/applications/apply/']['post']['requestBody']['content']
            ['application/json']['schema']['required'], ['game_alias'])

    def test_documentation_and_notification_routes_work(self):
        client = APIClient()
        self.assertEqual(client.get('/api/schema/').status_code, 200)
        self.assertEqual(client.get('/api/docs/').status_code, 200)
        user = User.objects.create_user('notice-user', 'notice@example.invalid', 'password')
        Notification.objects.create(user=user)
        client.force_authenticate(user)
        response = client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0], {'user': user.pk, 'mailing': None, 'viewed': False})

    def test_empty_matrix_is_not_a_completed_answer(self):
        for kind in (Question.Type.MATRIX, Question.Type.MATRIX_CHECKBOX):
            question = Question(type=kind)
            for value, filled in [(None, False), ([], False), ([[], []], False),
                                  ([['A'], []], False), ([['A'], ['B']], True)]:
                with self.subTest(kind=kind, value=value):
                    self.assertEqual(Answer(question=question, value=value).filled, filled)
