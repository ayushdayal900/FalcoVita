try:
    from passlib.hash import argon2
    print("Argon2 hash handler found")
    print("Backend:", argon2.get_backend())
    print("Hash:", argon2.hash("test"))
    print("Verification Success")
except Exception as e:
    print("Verification Failed")
    print(e)
