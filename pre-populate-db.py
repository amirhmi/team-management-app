from django.contrib.auth.models import User

from memberManagement.models import Team, UserProfile, Membership

members = [
    {"first_name": "Rick",
     "last_name": "Noval",
     "email": "noval@gmail.com",
     "phone_number": "+16048298769",
     "role": "AD"},

    {"first_name": "Susan",
     "last_name": "Conor",
     "email": "Susan@outlook.com",
     "phone_number": "+12125552368",
     "role": "RE"},

    {"first_name": "Margo",
     "last_name": "Barr",
     "email": "Barr@yahoo.com",
     "phone_number": "+16045298765",
     "role": "RE"},

    {"first_name": "Ronald",
     "last_name": "Lum",
     "email": "Lum@ubc.com",
     "phone_number": "+16048238764",
     "role": "AD"},

    {"first_name": "Melvin",
     "last_name": "Forbis",
     "email": "Forbis@gmail.com",
     "phone_number": "+16048298763",
     "role": "AD"},
]

team = Team.objects.create(name="course-team")
team.save()
for member in members:
    user = User.objects.create_user(username=member["email"], email=member["email"], first_name=member["first_name"],
                                    last_name=member["last_name"], password="1234")
    user_profile = UserProfile.objects.create(user=user, phone_number=member["phone_number"])
    membership = Membership.objects.create(team=team, user_profile=user_profile, role=member["role"])

    user.save()
    user_profile.save()
    membership.save()
