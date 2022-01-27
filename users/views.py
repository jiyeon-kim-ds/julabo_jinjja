from statistics import multimode
from xmlrpc.client import MultiCall
from django.http import JsonResponse
from django.core.exceptions import ValidationError 
from django.views import View
from django.shortcuts import render , redirect
from users.decorator import login_decorator
from users.models import User
from my_settings  import SECRET_KEY,ALGORITHM

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
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)

class LogInView(View):
    @login_decorator
    def post(self,request):
        data = json.loads(request.body) 
        try: 
            if not User.objects.filter(
                email           = data['email'],
                password        = data['password'],
                ).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'token':token}, status=200)

                #return redirect('loginpage')??   
            
        except KeyError:
            
            return render(request, '#로그인페이지???', data)

class CartView(View):
    @login_decorator
    def post(self,request):
        try:
            data       = json.loads(request.body)
            user_id    = request.user
            product_id = data['product_id']
            quantity   = data['quantity']
        
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message':'PRODUCT_NOT_EXIST'}, status=400)

            if not Option.objects.filter(id=product_id).exists():
                return JsonResponse({'message'})

            if quantity <= 0:
                return JsonResponse({'message':'QUANTITY_ERROR'}),

        except:
            

#class Cartlog(View):     
    #@login_decorator
    #def get(self,request):
        #user = request.user

        #if not Cart.objects.filter(user=user).exists():
            #return JsonResponse({'message':'CART_NOT_EXIST'}, status=400)