# CUSTOMER API endpoints
***
**endpoint:** /account/register/customer/
**methods:** (POST)
**view:** CustomerRegisterAPIView
**serializer:** CustomerRegisterSerializer

## REQUEST
```
{
    "email": "customer1@gmail.com",
    "password": "Zxcvbn1919*-",
    "password2": "Zxcvbn1919*-",
    "customeruser": {
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+905323456789"
    }
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 201,
    "message": "Your account has been successfully created",
    "data": {
        "email": "customer1@gmail.com",
        "username": "customer1",
        "is_active": true,
        "is_customer": true,
        "is_seller": false,
        "customeruser": {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+905323456789"
        },
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyMTczNTIxLCJpYXQiOjE2ODEzMDk1MjEsImp0aSI6IjY3ZjU0NWQ0ZjY3NTQ5NDM5NzZjNGFiMzA5ZTc0YjA5IiwidXNlcl9pZCI6Mn0.v-trnsJEVSMr--8hABAo-qo95S2K1n7B5CWJlbxbYTo"
    }
}
```
***
**endpoint:** /login/customer/
**methods:** (POST)
**view:** CustomerMyTokenObtainPairView
**serializer:** CustomerMyTokenObtainPairSerializer

## REQUEST
```
{
    "email": "customer1@gmail.com",
    "password": "Zxcvbn1919*-"
}
```

## RESPONSE
```
{
    "user": 2,
    "email": "customer1@gmail.com",
    "username": "customer1",
    "is_active": true,
    "is_customer": true,
    "is_seller": false,
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+905323456789",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyMTczNTY3LCJpYXQiOjE2ODEzMDk1NjcsImp0aSI6ImEwMjhmMTY0YTcxZDRmOTZhNTZlNGIzOTQ2NWM0MzZlIiwidXNlcl9pZCI6Mn0.fzJjQOhJyv4akfoPI9Fw1D_j1jyJOnDVpzARUSRdJM4",
    "default_shipping_address": null
}
```
***
**endpoint:** /account/customer/profile/
**methods:** (PUT)
**view:** CustomerProfileUpdateAPIView
**serializer:** CustomerProfileSerializer
**headers:** Authorization

## REQUEST
```
{
    "first_name": "Martin",
    "last_name": "Eden",
    "phone_number": "+905392121949"
}
```
`phone_number` is not **required** field:
```
{
    "first_name": "Martin",
    "last_name": "Eden"
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Your profile information has been successfully updated",
    "data": {
        "first_name": "Martin",
        "last_name": "Eden",
        "phone_number": "+905392121949"
    }
}
```
***
**endpoint:** /account/customer/address/
**methods:** (POST,PUT,DELETE)
**view:** AddressCreateUpdateDeleteAPIView
**serializer:** AddressSerializer
**headers:** Authorization

`"country":228` is equals **Turkey**

## POST REQUEST
```
{
    "address_name":"Home",
    "first_name":"John",
    "last_name":"Doe",
    "company_name":"ArtnCode",
    "phone_number":"+905391234567",
    "street_address_1":"Topcular Mah. Osman Gazi Cad.",
    "street_address_2":"Onur Apt. No:36/10",
    "postal_code":"34055",
    "city":"Eyupsultan",
    "city_area":"Istanbul",
    "country":228
}
```

## POST RESPONSE
```
{
    "status": "success",
    "code": 201,
    "message": "Your new address has been successfully created",
    "data": {
        "id": "c671e862-3a15-45a2-9a0c-ae790176feba",
        "address_name": "Home",
        "first_name": "John",
        "last_name": "Doe",
        "company_name": "ArtnCode",
        "phone_number": "+905391234567",
        "street_address_1": "Topcular Mah. Osman Gazi Cad.",
        "street_address_2": "Onur Apt. No:36/10",
        "postal_code": "34055",
        "city": "Eyupsultan",
        "city_area": "Istanbul",
        "country": 228
    }
}
```

## PUT REQUEST
```
{
    "id":"c671e862-3a15-45a2-9a0c-ae790176feba",
    "address_name":"My Home",
    "first_name":"Martin",
    "last_name":"Eden",
    "company_name":"",
    "phone_number":"+905393182715",
    "street_address_1":"Topcular Mah. Osman Gazi Cad.",
    "street_address_2":"No:2",
    "postal_code":"34055",
    "city":"Eyupsultan",
    "city_area":"Istanbul",
    "country":228
}
```



## PUT RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Your address has been successfully updated",
    "data": {
        "id": "c671e862-3a15-45a2-9a0c-ae790176feba",
        "address_name": "My Home",
        "first_name": "Martin",
        "last_name": "Eden",
        "company_name": "",
        "phone_number": "+905391234567",
        "street_address_1": "Topcular Mah. Osman Gazi Cad.",
        "street_address_2": "No:2",
        "postal_code": "34055",
        "city": "Eyupsultan",
        "city_area": "Istanbul",
        "country": 228
    }
}
```

## DELETE REQUEST
```
{
    "id":"e74b6bd3-837d-4a4e-84e1-fcd66d46d250"
}
```



## DELETE RESPONSE
```
{
    "status": "success",
    "code": 204,
    "message": "Your address deleted successfully",
    "data": []
}
```
***
**endpoint:** /account/customer/default/address/
**methods:** (PUT)
**view:** DefaultAddressUpdateAPIView
**serializer:** DefaultAddressSerializer
**headers:** Authorization

## REQUEST
```
{
    "default_shipping_address":"b1c9e37d-233a-49d3-839e-790efd2e1deb"
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Your default address has been successfully updated",
    "data": {
        "default_shipping_address": "b1c9e37d-233a-49d3-839e-790efd2e1deb"
    }
}
```
***
**endpoint:** /account/customer/addresses/
**methods:** (GET)
**view:** ListAddressAPIView
**serializer:** AddressSerializer
**headers:** Authorization

## RESPONSE
```
[
    {
        "id": "c671e862-3a15-45a2-9a0c-ae790176feba",
        "address_name": "My Home",
        "first_name": "Martin",
        "last_name": "Eden",
        "company_name": "",
        "phone_number": "+905391234567",
        "street_address_1": "Topcular Mah. Osman Gazi Cad.",
        "street_address_2": "No:2",
        "postal_code": "34055",
        "city": "Eyupsultan",
        "city_area": "Istanbul",
        "country": 228
    },
    {
        "id": "b1c9e37d-233a-49d3-839e-790efd2e1deb",
        "address_name": "Home Default",
        "first_name": "John",
        "last_name": "Doe",
        "company_name": "ArtnCode",
        "phone_number": "+905391234567",
        "street_address_1": "Topcular Mah. Osman Gazi Cad.",
        "street_address_2": "Onur Apt. No:36/10",
        "postal_code": "34055",
        "city": "Eyupsultan",
        "city_area": "Istanbul",
        "country": 228
    }
]
```

# SELLER API endpoints
***
**endpoint:** /account/register/seller/
**methods:** (POST)
**view:** SellerRegisterAPIView
**serializer:** SellerRegisterSerializer

## REQUEST
```
{
    "email": "seller1@gmail.com",
    "password": "Zxcvbn1919*-",
    "password2": "Zxcvbn1919*-",
    "selleruser": {
        "company_name": "ArtnCode Software",
        "phone_number": "+905393182798"
    }
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 201,
    "message": "Your account has been successfully created",
    "data": {
        "email": "seller1@gmail.com",
        "username": "seller1",
        "is_active": true,
        "is_customer": false,
        "is_seller": true,
        "selleruser": {
            "company_name": "ArtnCode Software",
            "seller_slug": "artncode-software",
            "code": "ARTN",
            "phone_number": "+905393182798"
        },
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyMTc2NTY1LCJpYXQiOjE2ODEzMTI1NjUsImp0aSI6IjA4MjBjODA5ZDI2NzQ4ZmNiNTk2OWU1N2I1Zjc5NGI0IiwidXNlcl9pZCI6M30.ULVVlHQ4SkOTujwqitVfwImB-tjm5AKcF8qAfSq7jIQ"
    }
}
```
***
**endpoint:** /login/seller/
**methods:** (POST)
**view:** SellerMyTokenObtainPairView
**serializer:** SellerMyTokenObtainPairSerializer

## REQUEST
```
{
    "email":"seller1@gmail.com",
    "password":"Zxcvbn1919*-"
}
```

## RESPONSE
```
{
    "user": 3,
    "email": "seller1@gmail.com",
    "username": "seller1",
    "is_active": true,
    "is_customer": false,
    "is_seller": true,
    "company_name": "ArtnCode Software",
    "company_image": "/images/account/sellers/default.png",
    "seller_slug": "artncode-software",
    "code": "ARTN",
    "phone_number": "+905393182798",
    "description": null,
    "website_url": null,
    "public_email": null,
    "public_phone_number": null,
    "fax_number": null,
    "street_address_1": null,
    "street_address_2": null,
    "postal_code": null,
    "city": null,
    "city_area": null,
    "country": null,
    "latitude": null,
    "longitude": null,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyMTc2NjU1LCJpYXQiOjE2ODEzMTI2NTUsImp0aSI6ImY5ZDM2NDJlZjJlNTQyZTk4ZjE4Mjg1ZmE4ZjgzZjJlIiwidXNlcl9pZCI6M30.DpGWaW1AA7okyd-HXB-JpBEWi4-JcrDjF3QZrQNntgk"
}
```
***
**endpoint:** /account/seller/profile/
**methods:** (PUT)
**view:** SellerProfileUpdateAPIView
**serializer:** SellerProfileSerializer
**headers:** Authorization

## REQUEST
```
{
    "company_name":"ArtnCode Software",
    "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Your profile information has been successfully updated",
    "data": {
        "company_name": "ArtnCode Software",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    }
}
```
***
**endpoint:** /account/seller/profile/slug/
**methods:** (PUT)
**view:** SellerSlugUpdateAPIView
**serializer:** SellerSlugSerializer
**headers:** Authorization

## REQUEST
```
{
    "seller_slug":"artncode"
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Your slug has been successfully updated",
    "data": {
        "seller_slug": "artncode"
    }
}
```
***
**endpoint:** /account/seller/profile/code/
**methods:** (PUT)
**view:** SellerCodeUpdateAPIView
**serializer:** SellerCodeSerializer
**headers:** Authorization

## REQUEST
```
{
    "code":"ARTC"
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Your company code has been successfully updated",
    "data": {
        "code": "ARTC"
    }
}
```
***
**endpoint:** /account/seller/profile/code/
**methods:** (PUT)
**view:** SellerCodeUpdateAPIView
**serializer:** SellerCodeSerializer
**headers:** Authorization

## REQUEST
```
{
    "code":"ARTC"
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Your company code has been successfully updated",
    "data": {
        "code": "ARTC"
    }
}
```
***
**endpoint:** /account/seller/contact/
**methods:** (PUT)
**view:** SellerContactUpdateAPIView
**serializer:** SellerContactSerializer
**headers:** Authorization

## REQUEST
```
{
    "website_url":"https://www.artncode.com",
    "public_email":"artncode_company@gmail.com",
    "public_phone_number":"+905391234567",
    "fax_number":"+905391234567"
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Your contact informations has been successfully updated",
    "data": {
        "website_url": "https://www.artncode.com",
        "public_email": "artncode_company@gmail.com",
        "public_phone_number": "+905391234567",
        "fax_number": "+905391234567"
    }
}
```
***
**endpoint:** /account/seller/location/
**methods:** (PUT)
**view:** SellerLocationUpdateAPIView
**serializer:** SellerLocationSerializer
**headers:** Authorization

After a successful *put request*, the `is_verified` field of **SellerUser** is updated to `True`

## REQUEST
```
{
    "street_address_1":"Osmanaga Mah. Bahariye Cad.",
    "street_address_2":"",
    "postal_code":"34714",
    "city":"Kadiköy",
    "city_area":"Istanbul",
    "country":228
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Your location informations has been successfully updated",
    "data": {
        "street_address_1": "Osmanaga Mah. Bahariye Cad.",
        "street_address_2": "",
        "postal_code": "34714",
        "city": "Kadiköy",
        "city_area": "Istanbul",
        "country": 228
    }
}
```
***
**endpoint:** /account/seller/company_image/
**methods:** (PUT)
**view:** SellerCompanyImageUpdateAPIView
**serializer:** SellerCompanyImageSerializer
**headers:** Authorization

## REQUEST

**Postman Settings:** Body > form-data
**Fields:**
- company_image (File): BMW.jpg

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Your company image has been successfully updated",
    "data": {
        "user": 3,
        "company_name": "ArtnCode Software",
        "company_image": "http://127.0.0.1:8000/images/account/sellers/seller1%40gmail.com/main_image.jpg"
    }
}
```
***
**endpoint:** /account/seller/profile/images/
**methods:** (POST, DELETE)
**view:** SellerMultipleImagesCreateAPIView
**serializer:** SellerCreateMultipleImageSerializer
**headers:** Authorization

## POST REQUEST

**Postman Settings:** Body > form-data
**Fields:**
- image_1 (File): AUDI.jpg
- image_2 (File): ASTON MARTIN.jpg
- image_3 (File): BENTLEY.jpg
- image_4 (File): FERRARI.jpg
- image_5 (File): MERCEDES BENZ.jpg

## POST RESPONSE
```
{
    "status": "success",
    "code": 201,
    "message": "Your images has been successfully created",
    "data": {
        "user": 3,
        "company_name": "ArtnCode Software",
        "images": [
            {
                "image_id": "d76c0af1-65f2-4ef6-b6f1-9b736465ad6b",
                "image": "/images/account/sellers/seller1%40gmail.com/d76c0af1-65f2-4ef6-b6f1-9b736465ad6b.jpg"
            },
            {
                "image_id": "7fe2cab6-f1be-43e7-b6b8-8bd05873333a",
                "image": "/images/account/sellers/seller1%40gmail.com/7fe2cab6-f1be-43e7-b6b8-8bd05873333a.jpg"
            },
            {
                "image_id": "4562a118-8f15-430a-9c5a-dc31d7362297",
                "image": "/images/account/sellers/seller1%40gmail.com/4562a118-8f15-430a-9c5a-dc31d7362297.jpg"
            },
            {
                "image_id": "7fca6361-a054-47fb-bc70-903223910b7d",
                "image": "/images/account/sellers/seller1%40gmail.com/7fca6361-a054-47fb-bc70-903223910b7d.jpg"
            },
            {
                "image_id": "be29a3a0-5eca-44b9-bd11-d52fa65858ce",
                "image": "/images/account/sellers/seller1%40gmail.com/be29a3a0-5eca-44b9-bd11-d52fa65858ce.jpg"
            }
        ]
    }
}
```

## DELETE REQUEST
```
...
```
## DELETE RESPONSE
```
...
```

# ACCOUNT API endpoints

*To try these actions, we must have an account with a valid email address.*

***
**endpoint:** /account/change-password/
**methods:** (PUT)
**view:** ChangePasswordView
**serializer:** ChangePasswordSerializer
**headers:** Authorization

## REQUEST
```
{
    "old_password":"Zxcvbn1919*-",
    "new_password":"venus1923*-",
    "new_password_confirm":"venus1923*-"
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Password updated successfully"
}
```
***
**endpoint:** /account/password-reset-email/
**methods:** (POST)
**view:** PasswordResetEmailAPIView
**serializer:** ForgotPasswordSerializer

## REQUEST
```
{
    "email":"uberke.karatas@gmail.com"
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Email send successfully",
    "email": "uberke.karatas@gmail.com",
    "uid": "NA",
    "token": "bmk9h1-2b6bf50027120df0801ad4b9a33fbb30"
}
```
***
**endpoint:** /account/password-set-update/
**methods:** (PUT)
**view:** SetNewPasswordAPIView
**serializer:** NewPasswordSerializer

## REQUEST
```
{
    "new_password":"Abcdef2023*-",
    "uidb64":"NA",
    "token":"bmk9h1-2b6bf50027120df0801ad4b9a33fbb30"
}
```

## RESPONSE
```
{
    "status": "success",
    "code": 200,
    "message": "Password updated successfully"
}
```