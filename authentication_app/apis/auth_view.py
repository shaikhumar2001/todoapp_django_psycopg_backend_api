from django.http import JsonResponse
from rest_framework.decorators import api_view
from common_utils.response_template import response_template
from common_utils.db_utils import DBHelper
from django.contrib.auth.hashers import make_password

# initialize
db = DBHelper()

@api_view(["GET"])
def login(request):
    return JsonResponse({
        "message": "Hello World"
    })

@api_view(["POST"])
def register(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """    
    try:
        d = request.data or {}
        # payload
        name = d.get("name")
        email = d.get("email")
        password = d.get("password")

        # validate payload
        payload_req = (
            ["name", name],
            ["email", email],
            ["password", password]
        )
        if not all(x[1] for x in payload_req):
            missing_fields = (x[0] for x in payload_req if not x[1])
            return response_template(
                success=False,
                error_code=400,
                message=f"Missing required fields: {", ".join(missing_fields)}",
                request=request,
                status=400
            )
        

        # check if email already exists
        chk_email_r = db.execute_query("SELECT user_id FROM todoapp.tusertbl WHERE email=%s", (email))
        if chk_email_r:
            return response_template(
                success=False,
                error_code=409,
                message="Email already registered",
                request=request,
                status=409
            )
        
        # create password hash
        password_hash = make_password(password=password, salt="todoapp_salt", hasher="sha256")

        # for testing --- 
        print(f"PASSWORD: {password}")
        print(f"PASSWORD_HASH: {password_hash}")

        # insert user
        insert_user_r = db.execute_query(
            """
                INSERT INTO todoapp.tusertbl
                    (name, email, password_hash)
                VALUES
                    (%s, %s, %s)
                RETURNING user_id
            """,
            [name,email,password_hash]
        )

        # check insert result
        if not insert_user_r:
            return response_template(
                success=False,
                error_code=500,
                message="Failed to register user",
                request=request,
                status=500
            )

        # success response
        return response_template(
            success=True,
            error_code=0,
            message="User registered successfully",
            data={"user_id": insert_user_r[0]["user_id"]},
            request=request,
            status=201
        )

    except Exception as e:
        return response_template(
            success=False,
            error_code=500,
            message=f"Internal server error: {e}",
            request=request
        )