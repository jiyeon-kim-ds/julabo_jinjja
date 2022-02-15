import re ,json ,jwt ,bcrypt

from django.http            import JsonResponse 
from django.views           import View

from users.models           import User
from django.conf            import settings 

REGEX_EMAIL = "^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$"
REGEX_PASSWORD = "^(?=.{8,16}$)(?=.*[a-z])(?=.*[0-9]).*$"

class SignUpView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)    
            firstname          = data['first_name']
            lastname           = data['last_name']
            email              = data['email']
            password           = data['password']

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message' : 'EMAIL_ALREADY_EXISTS'}, status=400)    
            
            if not re.match(REGEX_EMAIL , email):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status = 400)

            if not re.match(REGEX_PASSWORD , password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)

            hashed_password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                first_name            = firstname,
                last_name             = lastname,
                email                 = email,
                password              = hashed_password,
                
            )

            return JsonResponse({'message':'SUCCESS'},status=200)
    
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class LogInView(View):
    def post(self,request): 
        try: 
            data  = json.loads(request.body) 
            user  = User.objects.get(email=data['email'])
                
            if bcrypt.checkpw(data['password'].encode('utf-8'), User.password.encode('utf-8')):
               
               token = jwt.encode({'id': User.id}, settings.SECRET_KEY, settings.ALGORITHM)
               return JsonResponse({'token':token}, status=200)  
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"},status=400)




        
        