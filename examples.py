# Examples of how fill fields in requests

example_user = {
    "normal": {
        "summary": "Example with right correctly filled fields",
        "description": """1. Username must be unique\n
2. For your security create strong password:
Your password must be:\n
      a. at least 10 characters in length,\n
      b. at least 1 upper case,\n
      c. numeric, and special character """,
        "value": {
            "username": "tina99",
            "name": "Turkan",
            "surname": "Muradova",
            "password": "ms34Lp285"

        },
    },
    "Without any data": {
        "summary": "Example without any data. There is shown not required fields",
        "description": """1. Username must be unique\n
2. For your security create strong password:
Your password must be:\n
      a. at least 10 characters in length,\n
      b. at least 1 upper case,\n
      c. numeric, and special character """,
        "value": {
            "username": "tina99",
            "name": "Turkan",
            "surname": "",
            "password": "ms34Lp285"

        },
    },

}
