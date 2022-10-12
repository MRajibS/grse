import json
from helpers import *
from app import *
from app.Models import *
from flask.views import MethodView
from flask import current_app, Blueprint
from app.auth.admin_auth.utils import user_Required
from datetime import datetime
import datetime
from sqlalchemy import asc, desc
from app.m_models import *
from bson import json_util
users_view = Blueprint('user_view', __name__)
from bson.json_util import dumps
global current_timestamp
current_timestamp = datetime.datetime.now()


class Get_Employee_Details(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/EmployeeDetails.yaml', methods=['GET'])
    def get(self, employee_code):
        try:
            output = Get_Employee_details(employee_code)
            response = {"status": 'success', "message": 'Account details fetched successfully', "user_data": output}
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


class ScanFingerPrint(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/scanFingerPrint.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            terminal_id = request_data["terminal_id"]
            alpeta_user_id = request_data["alpeta_user_id"]
            alpeta_figerprint_id = request_data["alpeta_figerprint_id"]
            response = scanFingerPrint(terminal_id, alpeta_user_id, alpeta_figerprint_id)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


class ScanFaceData(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/ScanFaceData.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            terminal_id = request_data["terminal_id"]
            response = scanFaceData(terminal_id)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


class ScanCard(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/ScanCard.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            print(request_data)
            terminal_id = request_data["terminal_id"]
            response = scanCardData(terminal_id)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


class CreateUser(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/CreatUser.yaml', methods=['POST'])
    def post(self):
        try:
            alpeta_fingerprint_data_str = request.form["alpeta_fingerprint_data"]
            alpeta_fingerprint_data = json.loads(alpeta_fingerprint_data_str)

            apleta_card_data_str = request.form["alpeta_card_data"]
            apleta_card_data = json.loads(apleta_card_data_str)

            alpeta_face_data_str = request.form["alpeta_face_data"]
            alpeta_face_data = json.loads(alpeta_face_data_str)

            _user = Users.query.filter_by(employee_id=request.form["employee_id"]).first()
            if _user is None:
                try:
                    print("WHEN USER IS NONE")
                    usr_data = Users.addUser(employee_id=request.form["employee_id"],
                                             costcntr=request.form["costcntr"],
                                             vendor_id=request.form["vendor_id"],
                                             alpeta_user_id=request.form["alpeta_user_id"],
                                             designation_id=request.form["designation_id"],
                                             role_id=request.form["role_id"],
                                             shift_id=request.form["shift_id"],
                                             full_name=request.form["full_name"],
                                             dob=datetime.fromisoformat(request.form["dob"]),
                                             gender=request.form["gender"],
                                             nationality=request.form["nationality"],
                                             marital_status=request.form["marital_status"],
                                             address=request.form["address"],
                                             email=request.form["email"],
                                             phone=request.form["phone"],
                                             esi_no=request.form["esi_no"],
                                             pf_no=request.form["pf_no"],
                                             employment_type=request.form["employment_type"],
                                             # employment_start_date=datetime.fromisoformat(request.form["employment_start_date"]),
                                             # employment_end_date=datetime.fromisoformat(request.form["employment_end_date"]),
                                             # employment_separation_date = datetime.fromisoformat(request.form["employment_separation_date"]),
                                             password=request.form["password"],
                                             alpeta_password=request.form["alpeta_password"],
                                             #profile_picture=alpeta_face_data[1]['TemplateData'].split(",")[-1],
                                             auth_comb=request.form["AuthInfo"]
                                             )
                    print("LOCAL DB USER DATA INGESTION SUCCESSFUL")
                except Exception as e:
                    response = {"status": 'error', "message": str(e)}
                    return make_response(jsonify(response)), 200
                try:
                    print("ADDING FINGER PRINTS")
                    UserFPdata = []
                    for i in alpeta_fingerprint_data:
                        FP_obj1 = {"FingerID": i['FingerID'], "MinConvType": 3, "TemplateIndex": 1,
                                   "TemplateData": i['Template1']}
                        FP_obj2 = {"FingerID": i['FingerID'], "MinConvType": 3,
                                   "TemplateIndex": 2, "TemplateData": i['Template2']}
                        UserFPdata.append(FP_obj1)
                        UserFPdata.append(FP_obj2)
                        User_fingerprints.add_fingerprint(user_id=usr_data.id,
                                                          alpeta_user_id=request.form['alpeta_user_id'],
                                                          fingerid=i['FingerID'],
                                                          totalsize=i['TotalSize'],
                                                          template1=i['Template1'],
                                                          template2=i['Template2'],
                                                          convimage1=i['ConvImage1'],
                                                          convimage2=i['ConvImage2'])

                    print("LOCAL DB FINGER PRINTS INGESTION SUCCESSFUL")
                except Exception as e:
                    response = {"status": 'error', "message": str(e)}
                    return make_response(jsonify(response)), 200
                try:
                    print("ADDING CARD DATA")
                    card_record_create = User_cards.addCards(user_id=usr_data.id, cardnum=apleta_card_data['CardNum'])
                    print("LOCAL DB CARD DATA INGESTION SUCCESSFUL")
                except Exception as e:
                    response = {"status": 'error', "message": str(e)}
                    return make_response(jsonify(response)), 200

                # alpeta_face_data_str = request.form["alpeta_face_data"]
                # alpeta_face_data = json.loads(alpeta_face_data_str)

                try:
                    print("ADDING FACE DATA")
                    User_facedatas.AddFaceData(user_id=usr_data.id,
                                               templatesize=alpeta_face_data[0]['TemplateSize'],
                                               templatedata=alpeta_face_data[0]['TemplateData'],
                                               templatetype=alpeta_face_data[0]['TemplateType'])
                    print("LOCAL DB FACE DATA INGESTION SUCCESSFUL")
                except Exception as e:
                    print("FACE DATA ERROR")
                    response = {"status": 'error', "message": str(e)}
                    return make_response(jsonify(response)), 200

                # Post Data to alpeta server;
                print("ADDING DATA TO ALPETA SERVER")
                params = {
                    "UserInfo": {
                        "ID": str(usr_data.alpeta_user_id),
                        "UniqueID": str(usr_data.alpeta_user_id),
                        "Name": usr_data.full_name,
                        "AuthInfo": [9, 2, 0, 0, 0, 0, 0, 2],
                        # "AuthInfo": list_auth_info(request.form["AuthInfo"]),
                        "Privilege": 2,
                        "CreateDate": str(current_timestamp),
                        "UsePeriodFlag": 0,
                        "RegistDate": str(current_timestamp),
                        "ExpireDate": "2099-12-31 23:59:59",
                        "Password": request.form["password"],
                        "GroupCode": 0,
                        "AccessGroupCode": 0,
                        "UserType": 0,
                        "TimezoneCode": 0,
                        "BlackList": 0,
                        "FPIdentify": 1,
                        "FaceIdentify": 0,
                        "Partition": 0,
                        "APBExcept": 0,
                        "APBZone": 0,
                        "WorkCode": "****",
                        "MealCode": "****",
                        "MoneyCode": "****",
                        "MessageCode": 0,
                        "VerifyLevel": 0,
                        "PositionCode": 1000,
                        "Department": "",
                        "LoginPW": "",
                        "LoginAllowed": 0,
                        "Picture": alpeta_face_data[1]['TemplateData'],
                        "EmployeeNum": usr_data.employee_id,
                        "Email": usr_data.email,
                        "Phone": usr_data.phone
                    },
                    "UserFPInfo": UserFPdata,
                    "UserCardInfo": [{
                        "CardNum": apleta_card_data['CardNum']
                    }],
                    "UserFaceWTInfo": [{
                        "UserID": usr_data.alpeta_user_id,
                        "TemplateSize": alpeta_face_data[0]['TemplateSize'],
                        "TemplateData": alpeta_face_data[0]['TemplateData'],
                        "TemplateType": alpeta_face_data[0]['TemplateType']
                    }],
                }
                # print("JSON ", params)
                print("JSON CREATED SUCCESSFULLY")
                try:
                    url = f"{Settings.config.base_url}/users?UserID={request.form['alpeta_user_id']}"
                    print("SENDING REQUEST")
                    # print("JSON :", params)
                    req = requests.post(url, cookies=Login_cookie(), json=params)
                    # print("JSON :",jsonify(params))
                    status = req.status_code
                    content = json.loads(req.content.decode("utf-8"))
                    print("TOTAL CONTENT", content)
                    if status == 200:
                        ResultCode = content['Result']['ResultCode']
                        if ResultCode == 0:
                            response = {"status": 'success', "message": 'User created successfully', "user": content}
                            return make_response(jsonify(response)), 200
                        else:
                            User_fingerprints.Delete(usr_data.id)
                            User_cards.Delete(usr_data.id)
                            User_facedatas.Delete(usr_data.id)
                            Users.Delete(usr_data.id)
                            Users.query.filter(Users.employee_id == request.form["employee_id"]).update(
                                {Users.alpeta_user_id: None
                                 })
                            db.session.flush()
                            db.session.commit()

                            response = {"status": 'error',
                                        "message": f'Something went wrong in alpetaServer while selnding data, ResultCode {ResultCode}'}
                            return response
                    else:
                        User_fingerprints.Delete(usr_data.id)
                        User_cards.Delete(usr_data.id)
                        User_facedatas.Delete(usr_data.id)
                        Users.Delete(usr_data.id)
                        Users.query.filter(Users.employee_id == request.form["employee_id"]).update(
                            {Users.alpeta_user_id: None})
                        db.session.flush()
                        db.session.commit()
                        response = {"status": 'error',
                                    "message": f'Something went 'f'wrong in alpetaServer while '
                                               f'sending data, CONTENT {content} , Status code {status}'}
                        return response

                except Exception as e:
                    User_fingerprints.Delete(usr_data.id)
                    User_cards.Delete(usr_data.id)
                    User_facedatas.Delete(usr_data.id)
                    Users.Delete(usr_data.id)
                    Users.query.filter(Users.employee_id == request.form["employee_id"]).update(
                        {Users.alpeta_user_id: None
                         })
                    db.session.flush()
                    db.session.commit()
                    response = {"status": 'error', "message": str(e)}
                    return make_response(jsonify(response)), 200

            elif _user is not None and _user.alpeta_user_id is None:
                try:
                    try:
                        print("WHEN USER IS NOT NONE AND ALPETA USER ID IS NONE")
                        print("ADDING FINGER PRINTS")
                        UserFPdata = []
                        for i in alpeta_fingerprint_data:
                            FP_obj1 = {"FingerID": i['FingerID'], "MinConvType": 3, "TemplateIndex": 1,
                                       "TemplateData": i['Template1']}
                            FP_obj2 = {"FingerID": i['FingerID'], "MinConvType": 3,
                                       "TemplateIndex": 2, "TemplateData": i['Template2']}
                            UserFPdata.append(FP_obj1)
                            UserFPdata.append(FP_obj2)
                            User_fingerprints.add_fingerprint(user_id=_user.id,
                                                              alpeta_user_id=request.form['alpeta_user_id'],
                                                              fingerid=i['FingerID'],
                                                              totalsize=i['TotalSize'],
                                                              template1=i['Template1'],
                                                              template2=i['Template2'],
                                                              convimage1=i['ConvImage1'],
                                                              convimage2=i['ConvImage2'])
                        print("LOCAL DB FINGER PRINTS INGESTION SUCCESSFUL")
                    except Exception as e:
                        response = {"status": 'error', "message": str(e)}
                        return make_response(jsonify(response)), 200
                    try:
                        print("ADDING CARD DATA")
                        card_record_create = User_cards.addCards(user_id=_user.id,
                                                                 cardnum=apleta_card_data['CardNum'])
                        print("LOCAL DB CARD DATA INGESTION SUCCESSFUL")
                    except Exception as e:
                        response = {"status": 'error', "message": str(e)}
                        return make_response(jsonify(response)), 200
                    try:
                        print("ADDING FACE DATA")
                        User_facedatas.AddFaceData(user_id=_user.id,
                                                   templatesize=alpeta_face_data[0]['TemplateSize'],
                                                   templatedata=alpeta_face_data[0]['TemplateData'],
                                                   templatetype=alpeta_face_data[0]['TemplateType'])
                        print("LOCAL DB FACE DATA INGESTION SUCCESSFUL")
                    except Exception as e:
                        response = {"status": 'error', "message": str(e)}
                        return make_response(jsonify(response)), 200
                    try:
                        user_images.Add_profile_image(_user.id, alpeta_face_data[1]['TemplateData'], "active")
                        print("LOCAL DB PROFILE DATA INGESTION SUCCESSFUL")
                    except Exception as e:
                        response = {"status": 'error', "message": str(e)}
                        return make_response(jsonify(response)), 200
                    Users.query.filter(Users.employee_id == request.form["employee_id"]).update(
                        {Users.alpeta_user_id: request.form["alpeta_user_id"],
                         Users.costcntr: request.form["costcntr"] if request.form["costcntr"] else None,
                         Users.shift_id: request.form["shift_id"] if request.form["shift_id"] else None,
                         Users.designation_id: request.form["designation_id"] if request.form[
                             "designation_id"] else None,
                         Users.alpeta_password: request.form["alpeta_password"],
                         Users.password: request.form["password"] if request.form["password"] else None,
                         Users.alpeta_created_date: current_timestamp,
                         Users.alpeta_updated_date: current_timestamp,
                         Users.auth_comb: request.form["AuthInfo"],Users.registration_done:"Y"
                         })
                    db.session.flush()
                    db.session.commit()
                    print("PREPARING ALPETA JSON")
                    params = {
                        "UserInfo": {
                            "ID": str(_user.alpeta_user_id),
                            "UniqueID": str(_user.alpeta_user_id),
                            "Name": _user.full_name,
                            # "AuthInfo": [9, 2, 0, 0, 0, 0, 0, 2],
                            "AuthInfo": list_auth_info(request.form["AuthInfo"]),
                            "Privilege": 2,
                            "CreateDate": str(current_timestamp),
                            "UsePeriodFlag": 0,
                            "RegistDate": str(current_timestamp),
                            "ExpireDate": "2099-12-31 23:59:59",
                            "Password": request.form["password"],
                            "GroupCode": 0,
                            "AccessGroupCode": 0,
                            "UserType": 0,
                            "TimezoneCode": 0,
                            "BlackList": 0,
                            "FPIdentify": 1,
                            "FaceIdentify": 0,
                            "Partition": 0,
                            "APBExcept": 0,
                            "APBZone": 0,
                            "WorkCode": "****",
                            "MealCode": "****",
                            "MoneyCode": "****",
                            "MessageCode": 0,
                            "VerifyLevel": 0,
                            "PositionCode": 1000,
                            "Department": "",
                            "LoginPW": "",
                            "LoginAllowed": 0,
                            "Picture": alpeta_face_data[1]['TemplateData'],
                            "EmployeeNum": _user.employee_id,
                            "Email": _user.email,
                            "Phone": _user.phone
                        },
                        "UserFPInfo": UserFPdata,
                        "UserCardInfo": [{
                            "CardNum": apleta_card_data['CardNum']
                        }],
                        "UserFaceWTInfo": [{
                            "UserID": _user.alpeta_user_id,
                            "TemplateSize": alpeta_face_data[0]['TemplateSize'],
                            "TemplateData": alpeta_face_data[0]['TemplateData'],
                            "TemplateType": alpeta_face_data[0]['TemplateType']
                        }],
                    }
                    print("ALPETA JSON DATA CREATION SUCCESSFUL")
                    url = f"{Settings.config.base_url}/users?UserID={request.form['alpeta_user_id']}"
                    req = requests.post(url, cookies=Login_cookie(), json=params)
                    print("REQUEST SEND TO ALPETA SERVER")
                    status = req.status_code
                    content = json.loads(req.content.decode("utf-8"))
                    if status == 200:
                        ResultCode = content['Result']['ResultCode']
                        print("ALPETA SERVER RESPONSE RESULT CODE :", ResultCode)
                        if ResultCode == 0:
                            response = {"status": 'success', "message": "User Updated"}
                            return make_response(jsonify(response)), 200
                        else:
                            print("ELSE PART, IF RESULT CODE IS NOT 0")
                            User_fingerprints.Delete(_user.id)
                            User_cards.Delete(_user.id)
                            User_facedatas.Delete(_user.id)
                            Users.query.filter(Users.employee_id == request.form["employee_id"]).update(
                                {Users.alpeta_user_id: None})
                            db.session.flush()
                            db.session.commit()
                            response = {"status": 'error', "message": f'Something went'
                                                                      f'wrong in alpetaServer while '
                                                                      f'selnding data, ResultCode {ResultCode}'}
                        return response
                    else:
                        response = {"status": 'error',
                                    "message": f'Something went '
                                               f'wrong in alpetaServer while '
                                               f'selnding data, CONTENT {content} , Status code {status}'}
                        return response
                except Exception as e:
                    User_fingerprints.Delete(_user.id)
                    User_cards.Delete(_user.id)
                    User_facedatas.Delete(_user.id)
                    Users.query.filter(Users.employee_id == request.form["employee_id"]).update(
                        {Users.alpeta_user_id: None})
                    db.session.flush()
                    db.session.commit()
                    response = {"status": 'error', "message": f"{str(e)} : 'Something went wrong"}
                    return make_response(jsonify(response)), 200

            elif _user is not None and _user.alpeta_user_id is not None:
                response = {"status": 'error', "message": "User exists"}
                return make_response(jsonify(response)), 200
            else:
                response = {"status": 'error', "message": "Else error"}
                return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f"{str(e)} : 'Something went wrong"}
            return make_response(jsonify(response)), 200


class fn_View_Users_by_RoleID(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/AllUsers.yaml', methods=['POST'])
    def post(self, role_id, page):
        try:
            request_data = request.get_json(force=True)
            search_status = request_data["search_status"]
            Emoloyee_id = request_data["emoloyee_id"]
            Cost_Cntr = request_data["cost_cntr"] # changed 1 sept 2022 as CLMS Labour search by Aadhar (replace cost center column)
            Aadhar = request_data["aadhar"]
            Name = request_data["name"]
            export = request_data["export"]
            emoloyee_id = "%{}%".format(Emoloyee_id)
            CostCntr = "%{}%".format(Cost_Cntr)
            name = "%{}%".format(Name)
            aadhar = "%{}%".format(Aadhar)
            offset = int(10) * (int(page) - 1)
            Filter = request_data["Filter"]
            filter_params = request_data["filter_params"]

            if search_status == True and export != True and Filter != True:
                print("0",len(aadhar),aadhar)
                if len(Emoloyee_id) != 0:
                    print("emoloyee_id")
                    search_query = Users.query.filter(Users.status != 'delete',
                                                      Users.role_id == role_id,
                                                      Users.employee_id.like(emoloyee_id)).order_by(asc(Users.full_name)).all()
                    Userschema = User_schema(many=True)
                    output = Userschema.dump(search_query)
                    respone = {
                        "status": 'success',
                        "message": "Success",
                        "SearchCount": len(output),
                        "Users": Paginate(output, page)}
                    return make_response(jsonify(respone)), 200
                elif len(Cost_Cntr) != 0:
                    print("CostCntr")
                    # changed 1 sep 2022 as CLMS Labour search by Aadhar (replace cost center column)
                    search_query = Users.query.filter(Users.status != "delete",
                                                      Users.role_id == role_id,
                                                      Users.costcntr.like(CostCntr)).order_by(asc(Users.full_name)).all()
                    Userschema = User_schema(many=True)
                    output = Userschema.dump(search_query)
                    respone = {
                        "status": 'success',
                        "message": "Success",
                        "SearchCount": len(output),
                        "Users": Paginate(output, page)}
                    return make_response(jsonify(respone)), 200
                elif len(Aadhar) != 0:
                    print("aadhar")
                    # changed 1 sep 2022 as CLMS Labour search by Aadhar (replace cost center column)
                    search_query = Users.query.filter(Users.status != "delete",
                                                      Users.role_id == role_id,
                                                      Users.aadhaar.like(aadhar)).order_by(asc(Users.full_name)).all()
                    Userschema = User_schema(many=True)
                    output = Userschema.dump(search_query)
                    respone = {
                        "status": 'success',
                        "message": "Success",
                        "SearchCount": len(output),
                        "Users": Paginate(output, page)}
                    return make_response(jsonify(respone)), 200
                elif len(Name) != 0:
                    print("name")
                    test_query = db.session.execute(
                        f"SELECT * FROM users WHERE users.status != 'delete' AND users.role_id = {role_id} AND users.full_name ilike '%{Name}%'")
                    # print(test_query)
                    search_query = Users.query.filter(Users.status != "delete",
                                                      Users.role_id == role_id,
                                                      Users.full_name.like(name)).order_by(asc(Users.full_name)).all()
                    Userschema = User_schema(many=True)
                    output = Userschema.dump(test_query)
                    respone = {
                        "status": 'success',
                        "message": "Success",
                        "SearchCount": len(output),
                        "Users": Paginate(output, page)}
                    return make_response(jsonify(respone)), 200
                else:
                    respone = {"status": 'error', "message": "Error"}
                    return make_response(jsonify(respone)), 200

            elif search_status == True and export == True:
                print("1")
                if len(Emoloyee_id) != 0:
                    search_query = Users.query.filter(Users.status != 'delete',
                                                      Users.role_id == role_id,
                                                      Users.employee_id.like(emoloyee_id)).order_by(asc(Users.full_name)).all()
                    Userschema = User_schema(many=True)
                    output = Userschema.dump(search_query)
                    data = []

                    for i in output:
                        costcntr = i["costcntr"]
                        department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
                        if len(department_details) != 0:
                            shop_name = department_details["shop_name"]
                            i["shop_name"] = shop_name
                            data.append(i)
                        else:
                            i["shop_name"] = None
                            data.append(i)

                    respone = {
                        "status": 'success',
                        "message": "Success",
                        "SearchCount": len(output),
                        "Users": data}
                    return make_response(jsonify(respone)), 200
                elif len(Cost_Cntr) != 0:
                    print("2")
                    print("CostCntr")
                    search_query = Users.query.filter(Users.status != "delete",
                                                      Users.role_id == role_id,
                                                      Users.costcntr.like(CostCntr)).order_by(asc(Users.full_name)).all()
                    Userschema = User_schema(many=True)
                    output = Userschema.dump(search_query)
                    data = []

                    for i in output:
                        costcntr = i["costcntr"]
                        department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
                        if len(department_details) != 0:
                            shop_name = department_details["shop_name"]
                            i["shop_name"] = shop_name
                            data.append(i)
                        else:
                            i["shop_name"] = None
                            data.append(i)
                    respone = {
                        "status": 'success',
                        "message": "Success",
                        "SearchCount": len(output),
                        "Users": data}
                    return make_response(jsonify(respone)), 200
                elif len(Name) != 0:
                    print("3")
                    test_query = db.session.execute(
                        f"SELECT * FROM users WHERE users.status != 'delete' AND users.role_id = {role_id} AND users.full_name ilike '%{Name}%'")
                    # print(test_query)
                    search_query = Users.query.filter(Users.status != "delete",
                                                      Users.role_id == role_id,
                                                      Users.full_name.like(name)).all()
                    Userschema = User_schema(many=True)
                    output = Userschema.dump(test_query)
                    data = []

                    for i in output:
                        costcntr = i["costcntr"]
                        department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
                        if len(department_details) != 0:
                            shop_name = department_details["shop_name"]
                            i["shop_name"] = shop_name
                            data.append(i)
                        else:
                            i["shop_name"] = None
                            data.append(i)
                    respone = {
                        "status": 'success',
                        "message": "Success",
                        "SearchCount": len(output),
                        "Users": data}
                    return make_response(jsonify(respone)), 200
                elif len(aadhar) != 0:
                    print("aadhar")
                    # changed 1 sep 2022 as CLMS Labour search by Aadhar (replace cost center column)
                    search_query = Users.query.filter(Users.status != "delete",
                                                      Users.role_id == role_id,
                                                      Users.aadhaar.like(aadhar)).order_by(asc(Users.full_name)).all()
                    Userschema = User_schema(many=True)
                    output = Userschema.dump(search_query)
                    data = []

                    for i in output:
                        costcntr = i["costcntr"]
                        department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
                        if len(department_details) != 0:
                            shop_name = department_details["shop_name"]
                            i["shop_name"] = shop_name
                            data.append(i)
                        else:
                            i["shop_name"] = None
                            data.append(i)
                    respone = {
                        "status": 'success',
                        "message": "Success",
                        "SearchCount": len(output),
                        "Users": data}
                    return make_response(jsonify(respone)), 200
                else:
                    respone = {"status": 'error', "message": "Error"}
                    return make_response(jsonify(respone)), 200
            elif search_status == False and export != True and Filter != True:
                print("4")
                # query = Users.query.all()
                query = Users.query.filter(Users.role_id == role_id, Users.status != "delete").order_by(asc(Users.full_name)).limit(10).offset(10*int(page)-1)
                Userschema = User_schema(many=True)
                output = Userschema.dump(query)

                data = []

                for i in output:
                    costcntr = i["costcntr"]
                    department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
                    if len(department_details) != 0:
                        shop_name = department_details["shop_name"]
                        i["shop_name"] = shop_name
                        data.append(i)
                    else:
                        i["shop_name"] = None
                        data.append(i)

                respone = {"status": 'success', "message": "Success", "SearchCount": Users.query.filter(Users.role_id == role_id, Users.status != "delete").count(),
                           "Users": data
                }
                return make_response(jsonify(respone)), 200
            elif export == True and search_status == False and Filter == False:
                print("5")
                # query = Users.query.all()
                query = Users.query.filter(Users.role_id == role_id, Users.status != "delete").order_by(asc(Users.full_name)).all()
                Userschema = User_schema(many=True)
                output = Userschema.dump(query)

                data = []

                for i in output:
                    costcntr = i["costcntr"]
                    department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
                    if len(department_details) != 0:
                        shop_name = department_details["shop_name"]
                        i["shop_name"] = shop_name
                        data.append(i)
                    else:
                        i["shop_name"] = None
                        data.append(i)

                respone = {"status": 'success', "message": "Success", "SearchCount": len(data), "Users": data}
                return make_response(jsonify(respone)), 200
            elif Filter == True and search_status == False and export == True:
                print("filter 1")
                query_str = query_processor(filter_params, role_id,offset)
                print(query_str)
                query = db.session.execute(query_str)
                Userschema = User_schema(many=True)
                output = Userschema.dump(query)
                print(query_str)
                query2 = db.session.execute(query_str)
                Userschema = User_schema(many=True)
                output2 = Userschema.dump(query2)
                data = []
                for i in output:
                    costcntr = i["costcntr"]
                    department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
                    if len(department_details) != 0:
                        shop_name = department_details["shop_name"]
                        i["shop_name"] = shop_name
                        data.append(i)
                    else:
                        i["shop_name"] = None
                        data.append(i)

                respone = {"status": 'success', "message": "Success", "SearchCount": len(output2), "Users": data}
                return make_response(jsonify(respone)), 200
            elif Filter == True and search_status == False and export == False:
                print("filter 2")
                query_str = query_processor(filter_params, role_id,offset)
                print(query_str)
                query = db.session.execute(query_str + f" limit 10 offset {offset}")
                Userschema = User_schema(many=True)
                output = Userschema.dump(query)
                query2 = db.session.execute(query_str)
                Userschema = User_schema(many=True)
                output2 = Userschema.dump(query2)
                data = []
                for i in output:
                    costcntr = i["costcntr"]
                    department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
                    if len(department_details) != 0:
                        shop_name = department_details["shop_name"]
                        i["shop_name"] = shop_name
                        data.append(i)
                    else:
                        i["shop_name"] = None
                        data.append(i)

                respone = {"status": 'success', "message": "Success", "SearchCount": len(output2),
                           "Users": data}
                return make_response(jsonify(respone)), 200
            elif search_status == True and export != True and Filter == True:
                print("filter 3")
                query_str = query_processor(filter_params, role_id,offset)
                print(query_str)
                query = db.session.execute(query_str + f" limit 10 offset {offset}")
                Userschema = User_schema(many=True)
                output = Userschema.dump(query)
                query2 = db.session.execute(query_str)
                Userschema = User_schema(many=True)
                output2 = Userschema.dump(query2)
                data = []
                for i in output:
                    costcntr = i["costcntr"]
                    department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
                    if len(department_details) != 0:
                        shop_name = department_details["shop_name"]
                        i["shop_name"] = shop_name
                        data.append(i)
                    else:
                        i["shop_name"] = None
                        data.append(i)

                respone = {"status": 'success', "message": "Success", "SearchCount": len(output2),
                           "Users": data}
                return make_response(jsonify(respone)), 200

            elif Filter == True:
                print("filter 4")
                query_str = query_processor(filter_params, role_id, offset)
                print(query_str)
                query = db.session.execute(query_str + f" limit 10 offset {offset}")
                Userschema = User_schema(many=True)
                output = Userschema.dump(query)
                query2 = db.session.execute(query_str)
                Userschema = User_schema(many=True)
                output2 = Userschema.dump(query2)
                
                data = []
                for i in output:
                    costcntr = i["costcntr"]
                    department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
                    if len(department_details) != 0:
                        shop_name = department_details["shop_name"]
                        i["shop_name"] = shop_name
                        data.append(i)
                    else:
                        i["shop_name"] = None
                        data.append(i)

                respone = {"status": 'success', "message": "Success", "SearchCount": len(output2), "Users": data}
                return make_response(jsonify(respone)), 200
            else:
                respone = {"status": 'error', "message": "key 'Success' must ne True or Flase"}
                return make_response(jsonify(respone)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200

# class fn_View_Users_by_RoleID(MethodView):
#     @cross_origin(supports_credentials=True)
#     @swag_from('apidocs/AllUsers.yaml', methods=['POST'])
#     def post(self, role_id, page):
#         try:
#             request_data = request.get_json(force=True)
#             search_status = request_data["search_status"]
#             Emoloyee_id = request_data["emoloyee_id"]
#             Cost_Cntr = request_data["cost_cntr"] # changed 1 sept 2022 as CLMS Labour search by Aadhar (replace cost center column)
#             Aadhar = request_data["aadhar"]
#             Name = request_data["name"]
#             export = request_data["export"]
#             emoloyee_id = "%{}%".format(Emoloyee_id)
#             CostCntr = "%{}%".format(Cost_Cntr)
#             name = "%{}%".format(Name)
#             aadhar = "%{}%".format(Aadhar)
#             offset = int(10) * (int(page) - 1)
#             Filter = request_data["Filter"]
#             filter_params = request_data["filter_params"]

#             if search_status == True and export != True and Filter != True:
#                 print("0")
#                 if len(Emoloyee_id) != 0:
#                     print("emoloyee_id")
#                     search_query = Users.query.filter(Users.status != 'delete',
#                                                       Users.role_id == role_id,
#                                                       Users.employee_id.like(emoloyee_id)).order_by(asc(Users.full_name)).all()
#                     Userschema = User_schema(many=True)
#                     output = Userschema.dump(search_query)
#                     respone = {
#                         "status": 'success',
#                         "message": "Success",
#                         "SearchCount": len(output),
#                         "Users": Paginate(output, page)}
#                     return make_response(jsonify(respone)), 200
#                 elif len(Cost_Cntr) != 0:
#                     print("CostCntr")
#                     # changed 1 sep 2022 as CLMS Labour search by Aadhar (replace cost center column)
#                     search_query = Users.query.filter(Users.status != "delete",
#                                                       Users.role_id == role_id,
#                                                       Users.costcntr.like(CostCntr)).order_by(asc(Users.full_name)).all()
#                     Userschema = User_schema(many=True)
#                     output = Userschema.dump(search_query)
#                     respone = {
#                         "status": 'success',
#                         "message": "Success",
#                         "SearchCount": len(output),
#                         "Users": Paginate(output, page)}
#                     return make_response(jsonify(respone)), 200
#                 elif len(aadhar) != 0:
#                     print("aadhar")
#                     # changed 1 sep 2022 as CLMS Labour search by Aadhar (replace cost center column)
#                     search_query = Users.query.filter(Users.status != "delete",
#                                                       Users.role_id == role_id,
#                                                       Users.aadhaar.like(aadhar)).order_by(asc(Users.full_name)).all()
#                     Userschema = User_schema(many=True)
#                     output = Userschema.dump(search_query)
#                     respone = {
#                         "status": 'success',
#                         "message": "Success",
#                         "SearchCount": len(output),
#                         "Users": Paginate(output, page)}
#                     return make_response(jsonify(respone)), 200
#                 elif len(Name) != 0:
#                     test_query = db.session.execute(
#                         f"SELECT * FROM users WHERE users.status != 'delete' AND users.role_id = {role_id} AND users.full_name ilike '%{Name}%' ORDER BY users.full_name")
#                     # print(test_query)
#                     search_query = Users.query.filter(Users.status != "delete",
#                                                       Users.role_id == role_id,
#                                                       Users.full_name.like(name)).order_by(asc(Users.full_name)).all()
#                     Userschema = User_schema(many=True)
#                     output = Userschema.dump(test_query)
#                     respone = {
#                         "status": 'success',
#                         "message": "Success",
#                         "SearchCount": len(output),
#                         "Users": Paginate(output, page)}
#                     return make_response(jsonify(respone)), 200
#                 else:
#                     respone = {"status": 'error', "message": "Error"}
#                     return make_response(jsonify(respone)), 200

#             elif search_status == True and export == True:
#                 print("1")
#                 if len(Emoloyee_id) != 0:
#                     search_query = Users.query.filter(Users.status != 'delete',
#                                                       Users.role_id == role_id,
#                                                       Users.employee_id.like(emoloyee_id)).order_by(asc(Users.full_name)).all()
#                     Userschema = User_schema(many=True)
#                     output = Userschema.dump(search_query)
#                     data = []

#                     for i in output:
#                         costcntr = i["costcntr"]
#                         department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
#                         if len(department_details) != 0:
#                             shop_name = department_details["shop_name"]
#                             i["shop_name"] = shop_name
#                             data.append(i)
#                         else:
#                             i["shop_name"] = None
#                             data.append(i)

#                     respone = {
#                         "status": 'success',
#                         "message": "Success",
#                         "SearchCount": len(output),
#                         "Users": data}
#                     return make_response(jsonify(respone)), 200
#                 elif len(aadhar) != 0:
#                     print("aadhar")
#                     # changed 1 sep 2022 as CLMS Labour search by Aadhar (replace cost center column)
#                     search_query = Users.query.filter(Users.status != "delete",
#                                                       Users.role_id == role_id,
#                                                       Users.aadhaar.like(aadhar)).order_by(asc(Users.full_name)).all()
#                     Userschema = User_schema(many=True)
#                     output = Userschema.dump(search_query)
#                     data = []

#                     for i in output:
#                         costcntr = i["costcntr"]
#                         department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
#                         if len(department_details) != 0:
#                             shop_name = department_details["shop_name"]
#                             i["shop_name"] = shop_name
#                             data.append(i)
#                         else:
#                             i["shop_name"] = None
#                             data.append(i)
#                     respone = {
#                         "status": 'success',
#                         "message": "Success",
#                         "SearchCount": len(output),
#                         "Users": data}
#                     return make_response(jsonify(respone)), 200
#                 elif len(Cost_Cntr) != 0:
#                     print("2")
#                     print("CostCntr")
#                     # search_query = Users.query.filter(Users.status != "delete",
#                     #                                   Users.role_id == role_id,
#                     #                                   Users.costcntr.like(CostCntr)).order_by(asc(Users.full_name)).all()
#                     test_query = db.session.execute(
#                         f"SELECT * FROM users WHERE users.status != 'delete' AND users.role_id = {role_id} AND users.costcntr ilike '%{Cost_Cntr}%' ORDER BY users.full_name")
#                     Userschema = User_schema(many=True)
#                     output = Userschema.dump(test_query)
#                     data = []

#                     for i in output:
#                         costcntr = i["costcntr"]
#                         department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
#                         if len(department_details) != 0:
#                             shop_name = department_details["shop_name"]
#                             i["shop_name"] = shop_name
#                             data.append(i)
#                         else:
#                             i["shop_name"] = None
#                             data.append(i)
#                     respone = {
#                         "status": 'success',
#                         "message": "Success",
#                         "SearchCount": len(data),
#                         "Users": data}
#                     return make_response(jsonify(respone)), 200
#                 elif len(Name) != 0:
#                     print("3")
#                     test_query = db.session.execute(
#                         f"SELECT * FROM users WHERE users.status != 'delete' AND users.role_id = {role_id} AND users.full_name ilike '%{Name}%' ORDER BY users.full_name")
#                     Userschema = User_schema(many=True)
#                     output = Userschema.dump(test_query)
#                     data = []

#                     for i in output:
#                         costcntr = i["costcntr"]
#                         department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
#                         if len(department_details) != 0:
#                             shop_name = department_details["shop_name"]
#                             i["shop_name"] = shop_name
#                             data.append(i)
#                         else:
#                             i["shop_name"] = None
#                             data.append(i)
#                     respone = {
#                         "status": 'success',
#                         "message": "Success",
#                         "SearchCount": len(output),
#                         "Users": data}
#                     return make_response(jsonify(respone)), 200
#                 else:
#                     respone = {"status": 'error', "message": "Error"}
#                     return make_response(jsonify(respone)), 200
#             elif search_status == False and export != True and Filter != True:
#                 print("4")
#                 # query = Users.query.all()
#                 query = Users.query.filter(Users.role_id == role_id, Users.status != "delete").order_by(asc(Users.full_name)).limit(10).offset(10*int(page)-1)
#                 Userschema = User_schema(many=True)
#                 output = Userschema.dump(query)

#                 data = []

#                 for i in output:
#                     costcntr = i["costcntr"]
#                     department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
#                     if len(department_details) != 0:
#                         shop_name = department_details["shop_name"]
#                         i["shop_name"] = shop_name
#                         data.append(i)
#                     else:
#                         i["shop_name"] = None
#                         data.append(i)
#                 respone = {"status": 'success', "message": "Success", "SearchCount": Users.query.filter(Users.role_id == role_id, Users.status != "delete").count(),
#                           "Users": data
#                 }
#                 return make_response(jsonify(respone)), 200
#             elif export == True and search_status == False and Filter == False:
#                 print("5")
#                 # query = Users.query.all()
#                 query = Users.query.filter(Users.role_id == role_id, Users.status != "delete").order_by(asc(Users.full_name)).all()
#                 Userschema = User_schema(many=True)
#                 output = Userschema.dump(query)

#                 data = []

#                 for i in output:
#                     costcntr = i["costcntr"]
#                     department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
#                     if len(department_details) != 0:
#                         shop_name = department_details["shop_name"]
#                         i["shop_name"] = shop_name
#                         data.append(i)
#                     else:
#                         i["shop_name"] = None
#                         data.append(i)

#                 respone = {"status": 'success', "message": "Success", "SearchCount": len(data), "Users": data}
#                 return make_response(jsonify(respone)), 200
#             elif Filter == True and search_status == False and export == True:
#                 print("filter 1")
#                 query_str = query_processor(filter_params, role_id,offset)
#                 print(query_str)
#                 query = db.session.execute(query_str + f" limit 10 offset {offset}")
#                 Userschema = User_schema(many=True)
#                 output = Userschema.dump(query)
#                 print(query_str)
#                 query2 = db.session.execute(query_str)
#                 Userschema = User_schema(many=True)
#                 output2 = Userschema.dump(query2)
#                 data = []
#                 for i in output:
#                     costcntr = i["costcntr"]
#                     department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
#                     if len(department_details) != 0:
#                         shop_name = department_details["shop_name"]
#                         i["shop_name"] = shop_name
#                         data.append(i)
#                     else:
#                         i["shop_name"] = None
#                         data.append(i)

#                 respone = {"status": 'success', "message": "Success", "SearchCount": len(output2), "Users": data}
#                 return make_response(jsonify(respone)), 200
#             elif Filter == True and search_status == False and export == False:
#                 print("filter 2")
#                 query_str = query_processor(filter_params, role_id,offset)
#                 print(query_str)
#                 query = db.session.execute(query_str + f" limit 10 offset {offset}")
#                 Userschema = User_schema(many=True)
#                 output = Userschema.dump(query)
#                 query2 = db.session.execute(query_str)
#                 Userschema = User_schema(many=True)
#                 output2 = Userschema.dump(query2)
#                 data = []
#                 for i in output:
#                     costcntr = i["costcntr"]
#                     department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
#                     if len(department_details) != 0:
#                         shop_name = department_details["shop_name"]
#                         i["shop_name"] = shop_name
#                         data.append(i)
#                     else:
#                         i["shop_name"] = None
#                         data.append(i)

#                 respone = {"status": 'success', "message": "Success", "SearchCount": len(output2),
#                           "Users": data}
#                 return make_response(jsonify(respone)), 200
#             elif search_status == True and export != True and Filter == True:
#                 print("filter 3")
#                 query_str = query_processor(filter_params, role_id,offset)
#                 print(query_str)
#                 query = db.session.execute(query_str + f" limit 10 offset {offset}")
#                 Userschema = User_schema(many=True)
#                 output = Userschema.dump(query)
#                 query2 = db.session.execute(query_str)
#                 Userschema = User_schema(many=True)
#                 output2 = Userschema.dump(query2)
#                 data = []
#                 for i in output:
#                     costcntr = i["costcntr"]
#                     department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
#                     if len(department_details) != 0:
#                         shop_name = department_details["shop_name"]
#                         i["shop_name"] = shop_name
#                         data.append(i)
#                     else:
#                         i["shop_name"] = None
#                         data.append(i)

#                 respone = {"status": 'success', "message": "Success", "SearchCount": len(output2),
#                           "Users": data}
#                 return make_response(jsonify(respone)), 200

#             elif Filter == True:
#                 print("filter 4")
#                 query_str = query_processor(filter_params, role_id, offset)
#                 print(query_str)
#                 query = db.session.execute(query_str + f" limit 10 offset {offset}")
#                 Userschema = User_schema(many=True)
#                 output = Userschema.dump(query)
#                 query2 = db.session.execute(query_str)
#                 Userschema = User_schema(many=True)
#                 output2 = Userschema.dump(query2)
                
#                 data = []
#                 for i in output:
#                     costcntr = i["costcntr"]
#                     department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
#                     if len(department_details) != 0:
#                         shop_name = department_details["shop_name"]
#                         i["shop_name"] = shop_name
#                         data.append(i)
#                     else:
#                         i["shop_name"] = None
#                         data.append(i)

#                 respone = {"status": 'success', "message": "Success", "SearchCount": len(output2), "Users": data}
#                 return make_response(jsonify(respone)), 200
#             else:
#                 respone = {"status": 'error', "message": "key 'Success' must ne True or Flase"}
#                 return make_response(jsonify(respone)), 200
#         except Exception as e:
#             import traceback
#             traceback.print_exc()
#             response = {"status": 'error', "message": f'{str(e)}'}
#             return make_response(jsonify(response)), 200


class fn_Delete_Employee(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/DeleteUsers.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            data = Users.Delete(request_data['id'])
            respone = {"status": 'success', "message": "User Deleted successfully", "Users": data}
            return make_response(jsonify(respone)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


class fn_SearchUser(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/SearchUser.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            data = Users.query.filter(Users.role_id == int(request_data["role_id"]),
                                      or_(Users.employee_id.like(request_data["employee_id"]),
                                          Users.full_name.like(request_data["name"]),
                                          Users.alpeta_user_id.like(request_data["alpeta_user_id"])
                                          ))
            Userschema = User_schema(many=True)
            output = Userschema.dump(data)
            respone = {"status": 'success', "message": "success", "Users": output}
            return make_response(jsonify(respone)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


class fn_Update_ProfilePIC(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/UpdateProfilePic.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            img_str = request_data['img_str']
            alpeta_id = request_data['alpeta_id']
            user_id = request_data['user_id']
            type = request_data['type']
            response = Update_USER_ProfilePIC(alpeta_id=alpeta_id, user_id=user_id, image_str=img_str, type=type)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


class fn_Update_Card(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/UpdateCardNum.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            alpeta_id = request_data['alpeta_id']
            user_id = request_data['user_id']
            card = request_data['cardnum']
            response = Update_USER_Card(alpeta_id=alpeta_id, user_id=user_id, cardnum=card)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


def ConvertUserFingerdataToDatabase(FPdata, user_finger_database, user_id, alpeta_id):
    UserFPdata = []
    update_finger = [each['FingerID'] for each in FPdata]
    database_finger = [each["fingerid"] for each in user_finger_database]
    list_of_delete_finger = list(set(database_finger) - set(update_finger))
    print("update_finger -", update_finger, "database_finger -", database_finger,
          "list_of_delete_finger -", list_of_delete_finger)
    if list_of_delete_finger:
        for each in list_of_delete_finger:
            User_fingerprints.query.filter_by(user_id=user_id, fingerid=each).delete()
            db.session.commit()
    for i in FPdata:
        # print(FPdata)
        FP_obj1 = {"FingerID": i['FingerID'], "MinConvType": 3, 'Reserved': 0, "TemplateIndex": 1,
                   "TemplateData": i['Template1'], "UserID": str(alpeta_id)}
        FP_obj2 = {"FingerID": i['FingerID'], "MinConvType": 3, 'Reserved': 0,
                   "TemplateIndex": 2, "TemplateData": i['Template2'], "UserID": str(alpeta_id)}
        UserFPdata.append(FP_obj1)
        UserFPdata.append(FP_obj2)
        if i['FingerID'] in [each["fingerid"] for each in user_finger_database]:
            User_fingerprints.query.filter(User_fingerprints.user_id == user_id,
                                           User_fingerprints.fingerid == i['FingerID']).update({
                User_fingerprints.template1: i['Template1'],
                User_fingerprints.template2: i['Template2'],
                User_fingerprints.convimage1: i['ConvImage1'],
                User_fingerprints.convimage2: i['ConvImage2'],
                User_fingerprints.updated_at: current_timestamp
            })
            db.session.flush()
            db.session.commit()
            Users.query.filter(Users.employee_id == str(alpeta_id)).update(
                {
                    Users.alpeta_updated_date: current_timestamp
                })
            db.session.flush()
            db.session.commit()
        else:
            User_fingerprints.add_fingerprint(user_id=user_id,
                                              alpeta_user_id=alpeta_id,
                                              fingerid=i['FingerID'],
                                              totalsize=i['TotalSize'],
                                              template1=i['Template1'],
                                              template2=i['Template2'],
                                              convimage1=i['ConvImage1'],
                                              convimage2=i['ConvImage2'])
            db.session.flush()
            db.session.commit()
            Users.query.filter(Users.employee_id == str(alpeta_id)).update(
                {
                    Users.alpeta_updated_date: current_timestamp
                })
            db.session.flush()
            db.session.commit()
    return UserFPdata


class Update_User(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/UpdateUser.yaml', methods=['POST'])
    def post(self):
        try:
            current_timestamp = datetime.datetime.now()
            request_data = request.get_json(force=True)
            user_id_alpeta = request_data['alpeta_id']
            user_id = request_data['user_id']
            fingerprint = request_data['alpeta_fingerprint_data']
            password = request_data['password']
            face = request_data['alpeta_face_data']
            update_type = request_data['type']  # type : face, finger , auth_comb, password
            auth_combination = request_data['auth_comb']
            user_ = Users.FetchUSerDetails_By_ID(user_id)  # get user details from database
            profile_image = user_images.FetchProfileImage(_user_id=user_id) # get profile image details from database
            user_face_database = User_facedatas.FetchUserfacedatas_By_ID(user_id)  # get user face details from database
            user_finger_database = User_fingerprints.FetchUserFingerPrintDetails_By_ID(user_id)  # get user finger
            # from database
            user_finger = convert_database_to_alpeta_formate(user_finger_database, user_id_alpeta)  # convert to Alp-eta
            # structure
            user_face = User_facedatas.FetchUserfacedatas_By_ID(user_id)  # get user face from database
            if user_:
                user_details_alpeta = get_user_details(user_id_alpeta)  # get user details Alp-eta
                user_finger_alpeta = get_user_finger(user_id_alpeta)  # get user finger details Alp-eta
                user_face_alpeta = get_user_face(user_id_alpeta)  # get user face details Alp-eta
                if user_details_alpeta['status'] == 'success':
                    user_info = user_details_alpeta['user_details']
                    card_info = user_info.get('UserCardInfo', [])
                    if card_info:
                        user_info['UserCardInfo'][0]['UserID'] = str(user_id_alpeta)
                    user_info['UserInfo']["Picture"] = profile_image.get("profile_picture", "")
                    if update_type == "finger":
                        try:
                            user_info['UserFPInfo'] == ConvertUserFingerdataToDatabase(fingerprint,
                                                                                       user_finger_database, user_id,
                                                                                       user_id_alpeta)
                        except Exception as e:
                            response = {"status": 'error', "message": str(e)}
                            return make_response(jsonify(response)), 200
                    if update_type == "face":
                        user_info["UserFaceWTInfo"] = [{
                            "UserID": str(user_id_alpeta),
                            "TemplateSize": face[0]['TemplateSize'],
                            "TemplateData": face[0]['TemplateData'],
                            "TemplateType": face[0]['TemplateType']
                        }]
                        if user_id == user_face_database["user_id"]:
                            print("face update")
                            User_facedatas.query.filter(User_facedatas.user_id == user_id).update({
                                User_facedatas.templatesize: face[0]['TemplateSize'],
                                User_facedatas.templatedata: face[0]['TemplateData'],
                                User_facedatas.templatetype: face[0]['TemplateType'],
                                User_facedatas.updated_at: current_timestamp
                            })
                            db.session.flush()
                            db.session.commit()
                            Users.query.filter(Users.employee_id == str(user_id_alpeta)).update(
                                {
                                    Users.alpeta_updated_date: current_timestamp
                                })
                            db.session.flush()
                            db.session.commit()
                        else:
                            print("face added")
                            User_facedatas.AddFaceData(user_id=user_id,
                                                       templatesize=face[0]['TemplateSize'],
                                                       templatedata=face[0]['TemplateData'],
                                                       templatetype=face[0]['TemplateType'])
                            Users.query.filter(Users.employee_id == str(user_id_alpeta)).update(
                                {
                                    Users.alpeta_updated_date: current_timestamp
                                })
                            db.session.flush()
                            db.session.commit()
                    if update_type == "password":
                        user_info['UserInfo']["Password"] = password
                        Users.query.filter(Users.employee_id == str(user_id_alpeta)).update(
                            {Users.password: password,
                             Users.updated_at: current_timestamp,
                             Users.alpeta_updated_date: current_timestamp
                             })
                        db.session.flush()
                        db.session.commit()
                    if update_type == "auth_comb":
                        user_info['UserInfo']['AuthInfo'] = list_auth_info(json.dumps(auth_combination))
                        Users.query.filter(Users.employee_id == str(user_id_alpeta)).update(
                            {Users.auth_comb: json.dumps(auth_combination),
                             Users.updated_at: current_timestamp,
                             Users.alpeta_updated_date: current_timestamp
                             })
                        db.session.flush()
                        db.session.commit()
                    # if not updated with updated_type else send default value from database or Alpeta-data
                    if update_type != "finger":
                        user_info['UserFPInfo'] = user_finger_alpeta['user_finger'].get('UserFPInfo', user_finger)
                    if update_type != "face":
                        user_info["UserFaceWTInfo"] = user_face_alpeta['user_face'].get("UserFaceWTInfo", [{
                            "UserID": user_face.get("user_id", str(user_id_alpeta)),
                            "TemplateSize": user_face.get("templatesize", ""),
                            "TemplateData": user_face.get("templatedata", ""),
                            "TemplateType": user_face.get("templatetype", "")
                        }])
                    if update_type != "password":
                        user_info['UserInfo']['Password'] = user_["password"]
                    if update_type != "auth_comb":
                        user_info['UserInfo']['AuthInfo'] = list_auth_info(user_["auth_comb"]) if user_[
                            "auth_comb"] else [
                            9, 2, 0, 0, 0, 0, 0, 2]
                    update_user_details = put_user_details(str(user_id_alpeta), user_info)
                    if user_:
                        if update_user_details['status'] == 'success':
                            # collect terminals for that user
                            download_to_terminal = User_terminals.Get_Terminals_by_userID_blacklist_status_(user_id)
                            for terminal_id in download_to_terminal:
                                assign_user = Assign_userToTerMiNaLs(terminal_id, user_id_alpeta)
                            respone = {"status": 'success',
                                       "message": "User updated successfully and downloaded with " + str(
                                           update_type),
                                       "user_update_details": update_user_details,
                                       "updated_type": str(update_type)}
                            return make_response(jsonify(respone)), 200
                        else:
                            respone = {"status": 'Error',
                                       "message": "User updated unsuccessfully " + str(
                                           update_type),
                                       "user_update_details": update_user_details,
                                       "updated_type": str(update_type)}
                            return make_response(jsonify(respone)), 200
                    else:
                        respone = {"status": 'Error', "message": "User updated unsuccessfully ",
                                   "user_update_details": "Error while updating user with " + str(
                                       update_type)}
                        return make_response(jsonify(respone)), 200
                else:
                    respone = {"status": 'error', "message": "Error updating user details or user not registered",
                               "user_update_details": user_details_alpeta}
                    return make_response(jsonify(respone)), 200
            else:
                respone = {"status": 'error', "message": "Error updating user details or user not registered in DB",
                           "user_update_details": user_}
                return make_response(jsonify(respone)), 200

        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


class fn_UserInfo_by_TerminalID(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/UserInfoBYTerminalID.yaml', methods=['GET'])
    def get(self, id):
        try:
            response = Get_USER_Info_from_TerminalID(id=id)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


def terminal_status(terminal):
    data = {}
    data["online"] = list()
    data["offline"] = list()
    data["nolog"] = list()
    db = database_connect_mongo()
    db = db["terminal_log"]
    offline = db.find({"Terminal_id": terminal, "Status": "Disconnected"}).limit(1).sort("Date", -1)
    online = db.find({"Terminal_id": terminal, "Status": "Connected"}).limit(1).sort("Date", -1)
    if len(json.loads(dumps(online))) != 0 and len(json.loads(dumps(offline))) != 0:
        offline = db.find({"Terminal_id": terminal, "Status": "Disconnected"}).limit(1).sort("Date", -1)
        online = db.find({"Terminal_id": terminal, "Status": "Connected"}).limit(1).sort("Date", -1)
        if json.loads(dumps(online[0]))["Date"] > json.loads(dumps(offline[0]))["Date"]:
            data["online"].append(json.loads(dumps(online[0]))["Terminal_id"])
        else:
            data["offline"].append(json.loads(dumps(online[0]))["Terminal_id"])
    else:
        data["nolog"].append(terminal)
    return data
    

class User_CompleteDetails(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/UserCompleteDetails.yaml', methods=['GET'])
    def get(self, id):
        try:
            current_timestamp = datetime.datetime.now()
            department_id = None
            shift_id = None
            designation_id = None
            costcntr = None
            user_id = None
            UserDetails = Users.FetchUSerDetails_By_ID(_id=id)
            if UserDetails:
                user_id = UserDetails.get("id", None)
                costcntr = UserDetails.get("costcntr", None)
                shift_id = UserDetails.get("shift_id", None)
                designation_id = UserDetails.get("designation_id", None)
            department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
            UserDetails["profile_picture"] = user_images.FetchProfileImage(_user_id=user_id).get("profile_picture", "")
            UserDetails["unique_id"] = cr_dd.get_demog_value_by_demog_value(UserDetails["aadhaar"])["unique_id"] if \
                cr_dd.get_demog_value_by_demog_value(UserDetails["aadhaar"]) else None
            if department_details:
                department_id = department_details.get("id")
                shop_name = department_details.get("shop_name")

            TerminalID = User_terminals.Get_Terminals_by_userID(user_id)
            TerminalDetails = []
            terminal_details = []
            _group_id = []
            for i in TerminalID:
                T_data = Terminals.FetchTerminals_By_ID(i)
                T_data["status"] = "active" if T_data["alpeta_terminal_id"] in terminal_status(T_data["alpeta_terminal_id"])["online"] \
                    else "inactive"
                TerminalDetails.append(T_data)

            for i in TerminalDetails:
                group_id = Group_terminals.GET_GroupID_BY_terminalID(i["alpeta_terminal_id"])
                group_details = Group.FetchGroupDetails_By_ID(UserDetails.get("group_id", None))
                _group_id.append(group_details)
                print(_group_id)
                UserTerminals = User_terminals.Get_Terminals_by_userID_status(user_id)
                for each in UserTerminals:
                    if i['id'] == each["terminal_id"]:
                        i["user_terminal_id"] = each["id"]
                        i['is_block'] = each["is_block"]
                        i['user_terminal_updated_at'] = each["updated_at"]
                        i['user_terminal_created_at'] = each["created_at"]
                    terminal_details.append(i)

            DepartmentDetails = Department.FetchDEpartmentDetails_By_ID(department_id)
            ShiftDetails = Shifts.FetchShiftsDetails_By_ID(shift_id)
            DEsignationDetails = Designations.FetchDesignationDetails_By_ID(designation_id)
            FingerPrintDetails = User_fingerprints.FetchUserFingerPrintDetails_By_ID(user_id)
            CardData = User_cards.FetchUserCardsDetails_By_ID(user_id)
            FaceData = User_facedatas.FetchUserfacedatas_By_ID(user_id)
            details_json = {"UserDetails": UserDetails, "DepartmentDetails": DepartmentDetails,
                            "ShiftDetails": ShiftDetails, "DEsignationDetails": DEsignationDetails,
                            "FingerPrintDetails": FingerPrintDetails, "CardData": CardData,
                            "FaceData": FaceData, "TerminalDetails": TerminalDetails, "Group_info": _group_id[-1] if
                _group_id else None}

            response = {"status": 'success', "message": 'Details fetched successfully', "user_data": details_json}
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200

class LoginUserView(MethodView):
    @cross_origin(supports_credentials=True)
    #@swag_from('apidocs/login.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            user = Users.query.filter_by(employee_id=request_data["employee_id"]).first()
            if not user and user.role_id != 3:
                response = {"success": "error",
                            "status": 401,
                            "Message": "The employee_id you provided is not associated with this account or "
                                       "user not AUTHORISED"}
                return make_response(jsonify(response)), 200

            if user.employee_id == request_data["employee_id"] and bcrypt.check_password_hash(user.password,
                                                                                              request_data["password"]):
                expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=365)
                token = jwt.encode({'exp': expiration_time,
                                    "employee_id": request_data["employee_id"],
                                    "id": user.id},
                                   current_app.config['USER_SECRET_KEY'], algorithm='HS256')
                print(user.id)
                admin_details = Users.FetchUSerDetails_By_ID(user.id)
                response = {"status": "success",
                            "message": "Logged In Successfully",
                            "token": token,
                            # "token": token.decode("utf-8"),
                            "user_details": admin_details}
                return make_response(jsonify(response)), 200
            elif user.Password != request_data["Password"]:
                response = {"success": "error", "status": 401, "Message": "Invalid Password"}
                return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(str(e))
            response = {"success": "error", "status": 401,
                        "Message": "Try checking Your Credentials and Try again", "error": str(e)}
            return make_response(jsonify(response)), 200


class User_User_CompleteDetails(MethodView):
    @user_Access
    @cross_origin(supports_credentials=True)
    #@swag_from('apidocs/UserCompleteDetails.yaml', methods=['POST'])
    def post(self):
        try:
            token = request.headers.get('token')
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            id = decoded_token["id"]
            department_id = None
            shift_id = None
            designation_id = None
            costcntr = None
            user_id = None
            UserDetails = Users.FetchUSerDetails_By_ID(_id=id)
            if UserDetails:
                user_id = UserDetails.get("id", None)
                costcntr = UserDetails.get("costcntr", None)
                shift_id = UserDetails.get("shift_id", None)
                designation_id = UserDetails.get("designation_id", None)
            department_details = Department.FetchDEpartmentDetails_By_Cost_center(costcntr=costcntr)
            print(user_images.FetchProfileImage(_user_id=user_id).get("profile_picture", ""), user_id)
            UserDetails["profile_picture"] = user_images.FetchProfileImage(_user_id=user_id).get("profile_picture", "")
            if department_details:
                department_id = department_details.get("id")
                shop_name = department_details.get("shop_name")

            TerminalID = User_terminals.Get_Terminals_by_userID(user_id)
            TerminalDetails = []
            terminal_details = []
            _group_id = []
            for i in TerminalID:
                T_data = Terminals.FetchTerminals_By_ID(i)
                TerminalDetails.append(T_data)

            for i in TerminalDetails:
                group_id = Group_terminals.GET_GroupID_BY_terminalID(i["alpeta_terminal_id"])
                group_details = Group.FetchGroupDetails_By_ID(UserDetails.get("group_id", None))
                _group_id.append(group_details)
                print(_group_id)
                UserTerminals = User_terminals.Get_Terminals_by_userID_status(user_id)
                for each in UserTerminals:
                    if i['id'] == each["terminal_id"]:
                        i["user_terminal_id"] = each["id"]
                        i['is_block'] = each["is_block"]
                        i['user_terminal_updated_at'] = each["updated_at"]
                        i['user_terminal_created_at'] = each["created_at"]
                    terminal_details.append(i)

            DepartmentDetails = Department.FetchDEpartmentDetails_By_ID(department_id)
            ShiftDetails = Shifts.FetchShiftsDetails_By_ID(shift_id)
            DEsignationDetails = Designations.FetchDesignationDetails_By_ID(designation_id)
            FingerPrintDetails = User_fingerprints.FetchUserFingerPrintDetails_By_ID(user_id)
            CardData = User_cards.FetchUserCardsDetails_By_ID(user_id)
            FaceData = User_facedatas.FetchUserfacedatas_By_ID(user_id)
            details_json = {"UserDetails": UserDetails, "DepartmentDetails": DepartmentDetails,
                            "ShiftDetails": ShiftDetails, "DEsignationDetails": DEsignationDetails,
                            "FingerPrintDetails": FingerPrintDetails, "CardData": CardData,
                            "FaceData": FaceData, "TerminalDetails": TerminalDetails, "Group_info": _group_id[-1] if
                _group_id else None}

            response = {"status": 'success', "message": 'Details fetched successfully', "user_data": details_json}
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200


class User_Search_Attendance(MethodView):
    @user_Access
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/SearchAttendance.yaml', methods=['POST'])
    def post(self):
        try:
            token = request.headers.get('token')
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            nrdb = database_connect_mongo()
            nrdb = nrdb["all_attendance"]
            print("here")
            request_data = request.get_json(force=True)
            employee_id = decoded_token["employee_id"]  # Man number
            start_date = request_data['start_date']  # dd.mm.yyyy HH:MM:SS
            end_date = request_data['end_date']  # dd.mm.yyyy HH:MM:SS
            attendance_type = request_data['attendance']  # list ["P10","P20"]
            search_status = request_data['search_status']  # True or False
            page_no = request_data['pageno']  # Page No
            result = list()
            all_result = list()
            sort = list({'LDATE': -1}.items())
            if employee_id and start_date != end_date:
                Filter = {
                    'SATZA': {
                        '$in': attendance_type
                    },
                    'Raw.EventTime': {
                        '$gte': start_date,
                        '$lt': end_date
                    },

                    'PERNR': employee_id
                }
            elif employee_id and start_date == end_date:
                Filter = {
                    'SATZA': {
                        '$in': attendance_type
                    },
                    'Raw.EventTime': {
                        '$gte': start_date,
                    },

                    'PERNR': employee_id
                }
            elif start_date != end_date and not employee_id:
                Filter = {
                    'SATZA': {
                        '$in': attendance_type
                    },
                    'Raw.EventTime': {
                        '$gte': start_date,
                        '$lt': end_date
                    }
                }
            else:
                Filter = {
                    'SATZA': {
                        '$in': attendance_type
                    },
                    'Raw.EventTime': {
                        '$gte': start_date,
                    }
                }
            print(Filter,"@@@@@@@@@@@@@@@@@")
            all_data = nrdb.find(filter=Filter)
            for each in json.loads(json_util.dumps(all_data)):
                all_result.append(each)

            if search_status and request_data['export'] is False:
                data = nrdb.find(filter=Filter).limit(10).skip(10 * (page_no - 1))
                for each in json.loads(json_util.dumps(data)):
                    result.append(each)

            elif search_status is False and request_data['export']:
                data = nrdb.find(filter=Filter).limit(10).skip(10 * (page_no - 1))
                for each in json.loads(json_util.dumps(data)):
                    result.append(each)

            elif search_status and request_data['export']:
                data = nrdb.find(filter=Filter).limit(10).skip(10 * (page_no - 1))
                for each in json.loads(json_util.dumps(data)):
                    result.append(each)

            response = {"status": 'Success', "message": "Search Complete", "Search_count": len(result),
                        "All_Search_count": len(all_result),
                        "Search": result if len(result) != 0 else "Authlog not found for the "
                                                                  "following date",
                        "Total_search": all_result if request_data['export'] else []}
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200

class Update_User_Password(MethodView):
    # @user_Required
    @user_Access
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/UpdateAdminPass.yaml', methods=['POST'])
    def post(self):
        try:
            token = request.headers.get('token')
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            request_data = request.get_json(force=True)
            user_id = decoded_token["id"]
            password = request_data["password"]

            Users.query.filter(Users.id == user_id).update(
                {Users.password: bcrypt.generate_password_hash(password).decode('utf-8'),
                 Users.last_update_date: datetime.datetime.now()})
            db.session.flush()
            db.session.commit()

            response = {"status": 'success', "message": "Password updated successfully"}
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'error', "message": f'{str(e)}'}
            return make_response(jsonify(response)), 200
            
            
fn_View_Users_by_RoleID = fn_View_Users_by_RoleID.as_view("fn_View_Users")
Get_Employee_Details = Get_Employee_Details.as_view("Get_Employee_Details")
ScanFingerPrint = ScanFingerPrint.as_view("ScanFingerPrint")
ScanFaceData = ScanFaceData.as_view("ScanFaceData")
ScanCard = ScanCard.as_view("ScanCard")
CreateUser = CreateUser.as_view("CreateUser")
DeleteEmployee = fn_Delete_Employee.as_view("DeleteEmployee")
fn_SearchUser = fn_SearchUser.as_view("fn_SearchUser")
fn_Update_ProfilePIC = fn_Update_ProfilePIC.as_view("fn_Update_ProfilePIC")
fn_Update_Card = fn_Update_Card.as_view("fn_Update_Card")
fn_UserInfo_by_TerminalID = fn_UserInfo_by_TerminalID.as_view("fn_UserInfo_by_TerminalID")
User_CompleteDetails = User_CompleteDetails.as_view("User_CompleteDetails")
Update_User = Update_User.as_view("Update_User")
LoginUserView = LoginUserView.as_view('loginview')
User_User_CompleteDetails = User_User_CompleteDetails.as_view("User_User_CompleteDetails")
User_Search_Attendance = User_Search_Attendance.as_view("User_Search_Attendance")
Update_User_Password = Update_User_Password.as_view("Update_User_Password")
# # # adding routes to the Views we just created
users_view.add_url_rule('/user/all_users/<int:role_id>/<page>', view_func=fn_View_Users_by_RoleID, methods=['POST'])
users_view.add_url_rule('/user/employee_details/<employee_code>', view_func=Get_Employee_Details, methods=['GET'])
users_view.add_url_rule('/user/scanFingerPrint', view_func=ScanFingerPrint, methods=['POST'])
users_view.add_url_rule('/user/scanFaceData', view_func=ScanFaceData, methods=['POST'])
users_view.add_url_rule('/user/scanCard', view_func=ScanCard, methods=['POST'])
users_view.add_url_rule('/user/create_user', view_func=CreateUser, methods=['POST'])
users_view.add_url_rule('/user/delete_user', view_func=DeleteEmployee, methods=['POST'])
users_view.add_url_rule('/user/search', view_func=fn_SearchUser, methods=['POST'])
users_view.add_url_rule('/user/updateProfilePic', view_func=fn_Update_ProfilePIC, methods=['POST'])
users_view.add_url_rule('/user/updateCardNum', view_func=fn_Update_Card, methods=['POST'])
users_view.add_url_rule('/user/terminalUsers/info/<id>', view_func=fn_UserInfo_by_TerminalID, methods=['GET'])
users_view.add_url_rule('/user/userDetails/<int:id>', view_func=User_CompleteDetails, methods=['GET'])
users_view.add_url_rule('/user/updateUserDetails', view_func=Update_User, methods=['POST'])
users_view.add_url_rule('/user/login', view_func=LoginUserView, methods=['POST'])
users_view.add_url_rule('/user/useruserDetails', view_func=User_User_CompleteDetails, methods=['POST'])
users_view.add_url_rule('/user/search_attendance', view_func=User_Search_Attendance, methods=['POST'])
users_view.add_url_rule('/user/update_password', view_func=Update_User_Password, methods=['POST'])
