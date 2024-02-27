export const PRICES = [
  15,
  30,
  60,
  60,
  // energy
  60,
  100,
  200,
  400,
  800,
  1000,
  2000,
  3000,
  5000,
  10000,
  20000,
  40000
]

export const SPEED_COUNT = 4
export const BONUSES = [
  // SPEED
  [],
  [
    {
      matrix: 15,
      clones: [
        {
          count: 1,
          lvl: 0
        }
      ]
    },
    {
      matrix: 15,
      clones: [
        {
          count: 1,
          lvl: 0,
          global: true
        }
      ]
    }
  ],
  [
    {
      matrix: 60
    },
    {
      clones: [
        {
          count: 1,
          lvl: 0
        },
        {
          count: 1,
          lvl: 0,
          global: true
        },
        {
          count: 1,
          lvl: 1
        }
      ]
    },
    {
      clones: [
        {
          count: 1,
          lvl: 0,
          global: true
        },
        {
          count: 1,
          lvl: 0
        },
        {
          count: 1,
          lvl: 1,
          global: true
        }
      ]
    }
  ],
  [
    {
      energy: true
    },
    {
      energy: true
    },
    {
      matrix: 25
    }
  ],
  // ENERGY
  // 0
  [
    {
      matrix: 50
    }
  ],
  // 1
  [
    {
      matrix: 50,
      clones: [
        {
          count: 1,
          lvl: SPEED_COUNT + 0
        }
      ]
    }
  ],
  // 2
  [
    {
      matrix: 100,
      staking: 50,
      referal: 50
    }
  ],
  // 3
  [
    {
      matrix: 150,
      referal: 100,
      clones: [
        {
          count: 1,
          lvl: SPEED_COUNT + 0,
          global: true
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 1
        }
      ]
    }
  ],
  // 4
  [
    {
      matrix: 400,
      staking: 200,
      clones: [
        {
          count: 1,
          lvl: SPEED_COUNT + 0,
          global: true
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 0
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 1
        }
      ]
    },
    {
      referal: 100,
      clones: [
        {
          count: 1,
          lvl: SPEED_COUNT + 1,
          global: true
        },
        {
          count: 2,
          lvl: SPEED_COUNT + 0
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 1
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 2
        }
      ]
    }
  ],
  // 5
  [
    {
      matrix: 800,
      referal: 100,
      clones: [
        {
          count: 1,
          lvl: SPEED_COUNT + 0,
          global: true
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 0
        }
      ]
    }
  ],
  // 6
  [
    {
      matrix: 2000
    },
    {
      staking: 500,
      referal: 300
    }
  ],
  // 7
  [
    {
      referal: 200,
      matrix: 1800,
      clones: [
        {
          count: 1,
          lvl: SPEED_COUNT + 5
        }
      ]
    },
    {
      referal: 200,
      clones: [
        {
          count: 1,
          lvl: SPEED_COUNT + 4
        }
      ]
    }
  ],
  // 8
  [
    {
      referal: 500,
      matrix: 3000,
      staking: 1500
    }
  ],
  // 9
  [
    {
      referal: 600,
      matrix: 4500,
      clones: [
        {
          count: 1,
          lvl: SPEED_COUNT + 1
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 2,
          global: true
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 3
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 6
        },
        {
          count: 1,
          global: true,
          lvl: SPEED_COUNT + 3
        },
        {
          count: 1,
          global: true,
          lvl: SPEED_COUNT + 4
        },
        {
          count: 1,
          global: true,
          lvl: SPEED_COUNT + 5
        }
      ]
    }
  ],
  // 10
  [
    {
      matrix: 6000,
      staking: 2000,
      referal: 2000
    },
    {
      matrix: 4000,
      referal: 1000,
      clones: [
        {
          count: 1,
          lvl: SPEED_COUNT + 8
        }
      ]
    }
  ],
  // 11
  [
    {
      matrix: 25000,
      staking: 5000,
      referal: 5000,
      clones: [
        {
          count: 12,
          lvl: SPEED_COUNT + 0,
          global: true
        },
        {
          count: 10,
          lvl: SPEED_COUNT + 0
        },
        {
          count: 7,
          lvl: SPEED_COUNT + 1
        },
        {
          count: 3,
          lvl: SPEED_COUNT + 2
        },
        {
          count: 2,
          lvl: SPEED_COUNT + 3
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 4
        },
        {
          count: 1,
          lvl: SPEED_COUNT + 5
        }
      ]
    },
    {
      matrix: 40000
    },
    {
      matrix: 25000,
      referal: 5000,
      staking: 5000,
      clones: [
        {
          lvl: SPEED_COUNT + 6,
          count: 1,
          global: true
        },
        {
          lvl: SPEED_COUNT + 7,
          count: 1
        }
      ]
    }
  ]
]
