approval_config = {
    "rules": [
    {
        "conditons": [
            {
                "column": "amount",
                "columne_value": 10000,
                "operator": "lessthen",
                "column_value_type": "static",
            },
            {
                "column": "amount",
                "columne_value": 5000,
                "operator": "graterthen",
                "column_value_type": "static",
            },
            # {
            #     "column": "created_by",
            #     "columne_value": "Implementation Manager",
            #     "operator": "equal",
            #     "column_value_type": "role",
            # },
        ],
        "actions": [
            {
                "value": "Hiring Manager",
                "level": 3,
                "type": "role"
            },
            {
                "value": "HR",
                "level": 0,
                "type": "role"
            },
            {   
                "value": "990b0e98-0561-411e-aa65-51ad8023a3f4",
                "level": 0,
                "type": "static"
            }   
        ]
    },
]
}