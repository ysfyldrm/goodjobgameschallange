Overview
  leaderboard endpoints are accepting json and return json responses.
  
  /leaderboard/ (GET) gives all users in the database in json format.
  
  /leaderboard/{country_code}/ (GET) gives specific users from different country in the database in json format.
  
  /score/submit/{user_id}/ (PUT) takes json format, save score of user and adjusts the user ranks between changed user old point and new point value in database.
  
  example json format that /score/submit/{user_id}/ accepts:
  
    {
      "point": 5
    }
    
  /user/profile/{user_id}/ (GET) gives the specific user details in database in json format.
  
  /user/create/ (POST) takes single and multiple user detail json format, save the details in database and adjust the ranks below them.
  
  example json format that /user/create/ accepts:  
  
    {
        "point": 200,
        "display_name": "examplename",
        "country": "iso code"(2 character)
    }
    or 
    {
        "display_name": "examplename",
        "country": "iso code"(2 character)
    }
    or
    [{
        "point": 100,
        "display_name": "examplename",
        "country": "iso code"(2 character)
    },
    {
        "display_name": "examplename",
        "country": "iso code"(2 character)
    }]
