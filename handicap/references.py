state_abbr = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA",
              "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
              "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX",
              "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

states = ['ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO',
          'CONNECTICUT', 'WASHINGTON, DC', 'DELAWARE', 'FLORIDA', 'GEORGIA',
          'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS',
          'KENTUCKY', 'LOUISIANA', 'MAINE', 'MARYLAND', 'MASSACHUSETTS',
          'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA',
          'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO',
          'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA',
          'OREGON', 'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA',
          'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA',
          'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']

# https://www.usga.org/handicapping/roh/2020-rules-of-handicapping.html
# section 5.2a
initial_handicap_adjustments = {
    3: {'count': 1, 'adjustment': -2},
    4: {'count': 1, 'adjustment': -1},
    5: {'count': 1, 'adjustment': 0},
    6: {'count': 2, 'adjustment': -1},
    7: {'count': 2, 'adjustment': 0},
    8: {'count': 2, 'adjustment': 0},
    9: {'count': 3, 'adjustment': 0},
    10: {'count': 3, 'adjustment': 0},
    11: {'count': 3, 'adjustment': 0},
    12: {'count': 4, 'adjustment': 0},
    13: {'count': 4, 'adjustment': 0},
    14: {'count': 4, 'adjustment': 0},
    15: {'count': 5, 'adjustment': 0},
    16: {'count': 5, 'adjustment': 0},
    17: {'count': 6, 'adjustment': 0},
    18: {'count': 6, 'adjustment': 0},
    19: {'count': 7, 'adjustment': 0}
}
