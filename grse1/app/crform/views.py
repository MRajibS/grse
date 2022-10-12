from helpers import *
import concurrent.futures
from app import *
from app.Models import *
import operator
from flask.views import MethodView
from werkzeug.utils import secure_filename
from flask import current_app, Blueprint
from datetime import datetime
CRForm_view = Blueprint('cr_form_view', __name__)


class CreateCRForm(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/add_cr_form.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            form_name = request_data['form_name']
            form_shortcode = request_data['form_shortcode']
            form_description = request_data['form_description']
            form_heading = request_data['form_heading']
            form_slug = request_data['form_slug']
            form_sub_heading = request_data['form_sub_heading']
            status = request_data['status']
            cr_forms.Add_cr_form(form_name, form_shortcode, form_description, form_heading, form_slug, form_sub_heading,
                                 status)
            response = {
                "status": "success",
                "message": "CR Form created successfully"}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200

def form_permit(U):
    @wraps(U)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        request_data = request.form
        try:
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            print(decoded_token)
            # email = decoded_token['email']
            print("hello")
            #po_number = request_data["po_number"]
            cr_code = request_data.get('cr_code', None)

            print(cr_code,"cr_code")
            if not cr_code:
                form_id = request_data['form_id']
                form_shortcode = cr_forms.Fetch_cr_form_by_id(int(form_id))["form_shortcode"]
                costcenter = request_data.get('costcenter')
            else:
                form_shortcode = cr_code.split("_", 2)[1]
                costcenter = Cr_info.Fetch_cr_info(cr_code)[0]["cost_center"]
            CrFormMaster(form_shortcode, cr_code)

            # if email in Cache.cache.keys() and Cache.get(email) == token:
            init_by = Users.FetchUSerDetails_By_ID(decoded_token["id"])["employee_id"]
            print(init_by)
            # init_by = '415378'
            print("user Verified", init_by, CrFormMaster(form_shortcode, cr_code))
            # costcenter = request_data.get('costcenter', Cr_info.Fetch_cr_info(cr_code)[0]["cost_center"])

            print(costcenter, "11232")
            if Users.FetchUSerDetails_By_ID(decoded_token["id"])["role_id"]== 1:
                    print("Access granted")
                    return U(*args, **kwargs)
            
            if cr_code:
                #elif Users.FetchUSerDetails_By_ID(decoded_token["id"])["role_id"] != 1:
                form_id = request_data.get('form_id', Cr_info.Fetch_cr_info(cr_code)[0]["form_id"])
                Cr_info.Fetch_cr_info(cr_code)
                print("current state", [each["state"] for each in Cr_info.Fetch_cr_info(cr_code)][0])
                present_state = [each["state"] for each in Cr_info.Fetch_cr_info(cr_code)]
                present_status = [each["status"] for each in Cr_info.Fetch_cr_info(cr_code)]
                form_state_status = [each["form_state_status"] for each in Cr_info.Fetch_cr_info(cr_code)]
                print("current state", present_state)
                print("current status", present_status)
                next = finite_state_machine(present_state[0], permit(costcenter))
                print("next assignee", next)
                if present_status:
                    if present_status[0] != "correction" or present_status[0] == "complete":
                        print("admin role",Users.FetchUSerDetails_By_ID(decoded_token["id"])["role_id"],request_data.get('form_state', None),"here")
                        if form_state_status[0] == "release" and present_status[0] == "correction":
                            print("inside")
                            if init_by in next["previous_list"] or \
                                Users.FetchUSerDetails_By_ID(decoded_token["id"])["role_id"] == 1:
                                print("Access granted cause transfer", next["previous_list"],next["previous_state"])
                                return U(*args, **kwargs)
                            
                        elif init_by in next["next_list"] or \
                                Users.FetchUSerDetails_By_ID(decoded_token["id"])["role_id"] == '1':
                            print("Access granted", next["next_list"], next["next_state"])
                            return U(*args, **kwargs)
                        else:
                            return jsonify({"AUTH ERROR": "USER AUTHORISATION REQUIRED"}), 401
                    if present_status[0] == "correction":
                        # print("pre_list", next["previous_list"])
                        if init_by in next["previous_list"] or \
                                Users.FetchUSerDetails_By_ID(decoded_token["id"])["role_id"] == 1:
                            print("Access granted cause last state is correction", next["previous_list"],
                                  next["previous_state"])
                            return U(*args, **kwargs)
                        else:
                            return jsonify({"AUTH ERROR": "USER AUTHORISATION REQUIRED"}), 401
                    else:
                        if (init_by in next["previous_list"] and present_status[0] == "correction") \
                                or Users.FetchUSerDetails_By_ID(decoded_token["id"])["role_id"] == 1:
                            print("Access granted")
                            return U(*args, **kwargs)
                        else:
                            return jsonify({"AUTH ERROR": "USER AUTHORISATION REQUIRED"}), 401
                            
            
            elif not Cr_info.Fetch_cr_info(CrFormMaster(form_shortcode, cr_code)):
                # costcenter = CrFormMaster(form_shortcode, cr_code)
                print("permit level not", permit(costcenter))
                Cr_info.Fetch_cr_info(cr_code)
                # print("Cr_info", [each["state"] for each in Cr_info.Fetch_cr_info(cr_code)])
                # present_state = [each["state"] for each in Cr_info.Fetch_cr_info(cr_code)]
                print(finite_state_machine("clms_nodal_user", permit(costcenter)))
                if init_by in permit(costcenter)["clms_nodal_user"]:
                    print("Access granted", permit(costcenter)["clms_nodal_user"])
                    return U(*args, **kwargs)
                else:
                    print(1)
                    return jsonify({"AUTH ERROR": "USER AUTHORISATION REQUIRED"}), 401
            else:
                import traceback
                traceback.print_exc()
                print(2)
                print(Cr_info.Fetch_cr_info(CrFormMaster(form_shortcode, cr_code)))
                return jsonify({"AUTH ERROR": "USER AUTHORISATION REQUIRED"}), 401
        except:
            import traceback
            traceback.print_exc()
            print(3)
            return jsonify({"AUTH ERROR": "USER AUTHORISATION REQUIRED"}), 401

    return wrapper


class CreateCRForminit(MethodView):
    # @user_Required
    @form_permit
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/create_cr_form.yaml', methods=['POST'])
    def post(self):
        try:
            token = request.headers.get('token')
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            # print(decoded_token)
            next_as = None
            request_data = request.form
            cr_code = request_data.get('cr_code', None)
            # if 'form_state' not in request_data:
            form_state = request_data.get('form_state', "new")
            # form_state = "new"
            print(request_data.get('costcenter'))
            if int(decoded_token["id"]) != 1:
                designation_id = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["designation_id"]
                designation = Designations.FetchDesignationDetails_By_ID(designation_id)["name"]
                print(designation, "designation")

            # print(Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"])
            # form_id = request_data['form_id']
            # form_shortcode = cr_forms.Fetch_cr_form_by_id(int(form_id))["form_shortcode"]
            # CrFormMaster(form_shortcode, cr_code)
            # form_id = request_data.get('form_id', Cr_info.Fetch_cr_info(cr_code)[0]["form_id"])
            if not cr_code:
                form_id = request_data.get('form_id')
                costcenter = request_data.get('costcenter')
                po_number = request_data.get("po_number")
                form_shortcode = cr_forms.Fetch_cr_form_by_id(int(form_id))["form_shortcode"]
                dept = request_data.get('department')
                yard_no = request_data.get('yard_no')
                unit = request_data.get('unit')
                status = request_data.get("status")
            else:
                po_number = Cr_info.Fetch_cr_info(cr_code)[0]["po_number"]
                form_id = Cr_info.Fetch_cr_info(cr_code)[0]["form_id"]
                costcenter = Cr_info.Fetch_cr_info(cr_code)[0]["cost_center"]
                form_shortcode = cr_code.split("_", 2)[1]
                dept = Cr_info.Fetch_cr_info(cr_code)[0]["dept"]
                yard_no = Cr_info.Fetch_cr_info(cr_code)[0]["yard_no"]
                unit = Cr_info.Fetch_cr_info(cr_code)[0]["unit"]
                status = request_data.get("status", Cr_info.Fetch_cr_info(cr_code)[0]["status"])
                initiated_by = Cr_info.Fetch_cr_info_first(cr_code)
            CrFormMaster(form_shortcode, cr_code)

            #form_state = request_data["form_state"]
            init_by = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"]  # need to take from JWT
            form_status = request_data.get("form_status", "pending")
            # status = request_data.get("status", Cr_info.Fetch_cr_info(cr_code)[0]["status"])
            # unit = request_data.get('unit', Cr_info.Fetch_cr_info(cr_code)[0]["unit"])
            # po_number = request_data.get("po_number", Cr_info.Fetch_cr_info(cr_code)[0]["po_number"])
            attachment_code = request_data.get("attachment_code", None)
            if "dcode_details" in request_data.keys():
                dcode_details = json.loads(request_data.get("dcode_details", None))
            # print(request_data)
            # print(request.files)
            file_name = request.files.getlist('file[]')
            # print(file_name)
            # for file in file_name:
            #     print(file)

            # filename = secure_filename(file_name.filename)
            # path = save_file(file_name, filename)
            present_status = [each["status"] for each in Cr_info.Fetch_cr_info(cr_code)]
            present_state = [each["state"] for each in Cr_info.Fetch_cr_info(cr_code)]
            form_state_status = [each["form_state_status"] for each in Cr_info.Fetch_cr_info(cr_code)]
            if present_state:
                if present_status[0] != "correction" and present_status[0] != "rejected" :
                    if present_status[0] == "complete" and present_state[0] == 'clms_nodal_secu':
                        if Users.FetchUSerDetails_By_ID(decoded_token["id"])["role_id"] == 1 or form_state == "release":
                            
                            # final onboard
                            onboard = onboard_form(CrFormMaster(form_shortcode, cr_code), request_data)
                            if onboard["status"] != "Error":
                                Cr_info.Add_cr_info(dept, yard_no, initiated_by, unit, po_number,
                                                    costcenter,
                                                    "complete", form_id, CrFormMaster(form_shortcode, cr_code), "Admin",
                                                    "Admin" if form_state != "release" else init_by ,
                                                    "onboard" if form_state != "release" else "release",
                                                    Users.FetchUSerDetails_By_ID(decoded_token["id"])["employee_id"] if form_state != "release" else init_by ,
                                                datetime.now(), 1 if form_status == "rejected" else 0, init_by if form_state != "release" else init_by,
                                                request_data.get("remark", None),form_state,form_heading_concat(CrFormMaster(form_shortcode, cr_code)))
                                if form_state == "release":
                                    cr_dd.update_by_form_id(CrFormMaster(form_shortcode, cr_code), "cl_pass_valid_upto")

                                    cr_dd.Add_cr_dd("cl_pass_valid_upto", str(datetime.now().date()), init_by, request_data.get("remark", None),
                                                    init_by + "_" + "cl_pass_valid_upto" + "_" + str(datetime.now().date()),
                                                    init_by, CrFormMaster(form_shortcode, cr_code), "active")
                                                
                            response = {
                                "status": "success" if onboard["status"] != "Error" else "Error",
                                "message": "Approved by Admin" if onboard["status"] != "Error" else onboard["message"],
                                "output": onboard
                            }
                            print(response)
                            return make_response(jsonify(response)), 200
                        else:
                            response = {
                                "status": "error",
                                "message": "Admin Approval required"}
                            print(response)
                            return make_response(jsonify(response)), 200

                    else:
                        next_as = finite_state_machine(present_state[0], permit(costcenter))["next_state"]
                        print(present_state[0], "next state", next_as)
                elif form_state_status[0] == "release":
                    next_as = finite_state_machine(present_state[0], permit(costcenter))["previous_state"]
                    print(present_state[0], "previous state", next_as)
                elif present_status[0] == "correction":
                    next_as = finite_state_machine(present_state[0], permit(costcenter))["previous_state"]
                    print(present_state[0], "previous state", next_as)
                else:
                    next_as = finite_state_machine("clms_nodal_user", permit(costcenter))

            user_permit = Department.get_department_by_costcenter(costcenter)
            print("permit level", permit(costcenter))
            if "dcode_details" in request_data.keys():
                for each in json.loads(dcode_details):
                    if each["dcode"] and CrFormMaster(form_shortcode, cr_code):
                        # print("form_shortcode", form_shortcode, each)
                        cr_dd.update_by_form_id(CrFormMaster(form_shortcode, cr_code), each["dcode"])

                        cr_dd.Add_cr_dd(each["dcode"], each["d_value"], init_by, request_data.get("remark", None),
                                        init_by + "_" + each["dcode"] + "_" + str(datetime.now().date()),
                                        init_by, CrFormMaster(form_shortcode, cr_code), "active")
                    else:
                        cr_dd.Add_cr_dd(each["dcode"], each["d_value"], init_by, request_data.get("remark", None),
                                        init_by + "_" + each["dcode"] + "_" + str(datetime.now().date()),
                                        init_by, CrFormMaster(form_shortcode, cr_code), "active")

            if attachment_code:
                for code, file in zip(json.loads(json.loads(attachment_code)), file_name):
                    filename = secure_filename(file.filename)
                    if filename:
                        path = save_file(file, CrFormMaster(form_shortcode, cr_code) + "_" +
                                         str(datetime.now()).replace(" ", "_") + "." + filename.split(".")[1])
                    if cr_code:

                        media_doc.Add_media_doc(attachment_codes(cr_code, next_as if next_as else "clms_nodal_user"), code["details"],
                                                path.get("message", None),
                                                CrFormMaster(form_shortcode, cr_code),
                                                init_by, "active")
                    else:
                        media_doc.Add_media_doc(
                            attachment_codes(cr_code, next_as if next_as else "clms_nodal_user"),
                            code["details"],
                            path.get("message", None),
                            CrFormMaster(form_shortcode, cr_code),
                            init_by, "active")
            if not cr_code:
                Cr_info.Add_cr_info(dept, yard_no, init_by, unit, po_number,
                                    costcenter,
                                    status, form_id, CrFormMaster(form_shortcode, cr_code),designation,
                                    "clms_nodal_user",
                                    form_status, None, None, 0,init_by,request_data.get("remark", None), form_state,form_heading_concat(CrFormMaster(form_shortcode, cr_code)))
            elif cr_code and form_status == "rejected":
                Cr_info.update_by_form_id(CrFormMaster(form_shortcode, cr_code), form_status,
                                          1 if form_status == "rejected" else 0)
                print("next as", next_as)
                Cr_info.Add_cr_info(dept, yard_no, initiated_by, unit, po_number,
                                    costcenter,
                                    "rejected", form_id, CrFormMaster(form_shortcode, cr_code), designation, next_as,
                                    "rejected",
                                    None, None, 1, init_by,request_data.get("remark", None),form_state,form_heading_concat(CrFormMaster(form_shortcode, cr_code)))

            elif cr_code and next_as == "clms_nodal_secu" and status == "complete":
                Cr_info.Add_cr_info(dept, yard_no, initiated_by, unit, po_number,
                                    costcenter,
                                    status, form_id, CrFormMaster(form_shortcode, cr_code), designation, next_as,
                                    "complete",
                                    None, None, 0, init_by,request_data.get("remark", None),form_state,form_heading_concat(CrFormMaster(form_shortcode, cr_code)))
            else:
                # Cr_info.update_by_form_id(CrFormMaster(form_shortcode, cr_code), form_status,
                #                           1 if form_status == "rejected" else 0)
                Cr_info.Add_cr_info(dept, yard_no, init_by if not initiated_by else initiated_by, unit, po_number,
                                    costcenter,
                                    status, form_id, CrFormMaster(form_shortcode, cr_code), designation, next_as,
                                    form_status,
                                    None,
                                    None, 1 if form_status == "rejected" else 0, init_by,request_data.get("remark", None),form_state,form_heading_concat(CrFormMaster(form_shortcode, cr_code)))
            response = {
                "status": "success",
                "message": "CR Form submitted successfully by " + next_as if next_as  else "CR Form submitted successfully by clms_nodal_user"}
            print(response)
            return make_response(jsonify(response)), 200

        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200

class ViewCRForm(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/view_cr_form.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            cr_code = request_data['cr_code']
            if len(Cr_info.Fetch_cr_info(cr_code)) != 0:
                output = Cr_info.Fetch_cr_info(cr_code)[0]
                output["po_date"] = po_master.Fetch_po_with_po_number(output.get("po_number")).get("po_date")
                output["form_type"] = cr_forms.Fetch_cr_form(cr_code.split("_", 2)[1])
                output["doc_details"] = media_doc.get_document_by_form_id(cr_code)
                output["form_details"] = form_details(cr_code)
                output["last_submitted"] = last_submitted(cr_code)
                output["next_assigne"] = next_assigne(cr_code)
                output["form_log"] = form_state(cr_code)
                output["form_state"] = state_machine(cr_code)
                output["remark"] = fetch_remark(cr_code)
                response = {
                    "status": "success",
                    "message": "CR Form fetched successfully",
                    "Data": output
                }
            else:
                response = {
                    "status": "success",
                    "message": "CR Form data not found",
                    "Data": []
                }
            #print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            #print(response)
            return make_response(jsonify(response)), 200
            
# def is_prime(n,_init_by):
#     print(n["unique_id"],"unique-----")
#     if _init_by in finite_state_machine(n["state"], permit(n["cost_center"]))["previous_list"] and n["status"] == "correction" :
#         n["form_slug"] = "Form"+n["unique_id"].split("_", 2)[1]
#         n["edit"] = True
#         return n
#     elif _init_by in finite_state_machine(n["state"], permit(n["cost_center"]))[
#                         "next_list"] \
#                           and n["status"] != "correction":
#         n["form_slug"] = "Form"+n["unique_id"].split("_", 2)[1]
#         n["edit"] = True
#         return n
#     else:
#         pass

class CRForminit(MethodView):
    #@user_Access
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/view_cr_form.yaml', methods=['POST'])
    def post(self):
        try:
            token = request.headers.get('token')
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            access = list()
            request_data = request.get_json(force=True)
            #form_search = request_data['form_search']
            search = request_data['search']
            page_no = request_data['page_no']
            offset = int(10) * (int(page_no) - 1)
            #status = request_data['status']
            
            _init_by = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"]
            query = f"select clms_nodal_ajs,clms_nodal_secu,clms_nodal_hr,clms_nodal_user,hod_functional_area,hod_man from department where hod_functional_area = '{_init_by}' or hod_man = '{_init_by}'"
            query = db.session.execute(query)
            DeptSchema = Department_schema(many=True)
            result = DeptSchema.dump(query)
            if result:
                result = list(set(map(operator.itemgetter('clms_nodal_ajs','clms_nodal_hr','clms_nodal_user','clms_nodal_secu','hod_man','hod_functional_area'), result)))[0]
                result = list(result)
                result.append(_init_by)
            else:
                result = [_init_by,_init_by]
            
            
            # if not result:
            #     result = (_init_by)
            print("result-------",result)
            
            query_3 = f"select DISTINCT ON(cr_info.unique_id) cr_info.id from cr_info order by " \
                      f"cr_info.unique_id asc,cr_info.created_at desc "
            query_3 = db.session.execute(query_3)
            CrInfoSchema = cr_info_schema(many=True)
            access_form = CrInfoSchema.dump(query_3)
            form_id_list = list()
            access_form = [int(a_dict["id"])for a_dict in access_form]
            print(access_form)
            if search:
                query_2 = f"select * from cr_info where cr_info.id in {tuple(access_form)} and " \
                          f"cr_info.form_status in ('initiated', 'pending') and exists (select * from department where " \
                          f"cr_info.cost_center = department.costcntr and (department.hod_man in {tuple(i for i in result)} or " \
                          f"department.hod_functional_area in {tuple(i for i in result)} or (department.clms_nodal_user in {tuple(i for i in result)} and " \
                          f"((cr_info.state = 'clms_nodal_ajs' and cr_info.status = 'correction'))) or " \
                          f"(department.clms_nodal_ajs in {tuple(i for i in result)} and ((cr_info.state = 'clms_nodal_user' " \
                          f"and cr_info.status = 'complete') or (cr_info.state = 'clms_nodal_hr' " \
                          f"and cr_info.status = 'correction')))or (department.clms_nodal_hr in {tuple(i for i in result)} and " \
                          f"((cr_info.state = 'clms_nodal_ajs' and cr_info.status = 'complete') or " \
                          f"( cr_info.state = 'clms_nodal_secu' and cr_info.status = 'correction'))) or " \
                          f"(department.clms_nodal_secu in {tuple(i for i in result)} and ((cr_info.state = 'clms_nodal_hr' " \
                          f"and cr_info.status = 'complete'))))) and (cr_info.form_heading ILIKE '%{search}%' OR cr_info.unique_id ILIKE '%{search}%') limit 10 offset {offset}"
            else:
                query_2 = f"select * from cr_info where cr_info.id in {tuple(access_form)} and " \
                          f"cr_info.form_status in ('initiated', 'pending') and exists (select * from department where " \
                          f"cr_info.cost_center = department.costcntr and (department.hod_man in {tuple(i for i in result)} or " \
                          f"department.hod_functional_area in {tuple(i for i in result)} or (department.clms_nodal_user in {tuple(i for i in result)} and " \
                          f"((cr_info.state = 'clms_nodal_ajs' and cr_info.status = 'correction'))) or " \
                          f"(department.clms_nodal_ajs in {tuple(i for i in result)} and ((cr_info.state = 'clms_nodal_user' " \
                          f"and cr_info.status = 'complete') or (cr_info.state = 'clms_nodal_hr' " \
                          f"and cr_info.status = 'correction')))or (department.clms_nodal_hr in {tuple(i for i in result)} and " \
                          f"((cr_info.state = 'clms_nodal_ajs' and cr_info.status = 'complete') or " \
                          f"( cr_info.state = 'clms_nodal_secu' and cr_info.status = 'correction'))) or " \
                          f"(department.clms_nodal_secu in {tuple(i for i in result)} and ((cr_info.state = 'clms_nodal_hr' " \
                          f"and cr_info.status = 'complete')))))limit 10 offset {offset}"
            print(query_2)
            query_2 = db.session.execute(query_2)
            CrInfoSchema = cr_info_schema(many=True)
            access_user = CrInfoSchema.dump(query_2)
            
            if "employee_id" in decoded_token.keys(): # ignore admin
                permit_ = Department.check_ROW_if_exists_in_Table(str(decoded_token["employee_id"]))
            response = {
                "permission": Department.check_ROW_if_exists_in_Table(str(decoded_token["employee_id"])) if "employee_id" in decoded_token.keys() else False,
                "message": "CR Form fetched successfully",
                "access_form": access_user,
                "count": len(access_user)
            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200

class CRForminitSubmitted(MethodView):
    @user_Access
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/view_cr_form.yaml', methods=['POST'])
    def post(self):
        try:
            token = request.headers.get('token')
            request_data = request.get_json(force=True)
            page_no = request_data['page_no']
            #form_search = request_data['form_search']
            search = request_data['search']
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            _init_by = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"]
            print("_init_by----------",_init_by)
            offset = int(10) * (int(page_no) - 1)
            access = list()
            permit_ =[]
            _init_by = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"]
            query = f"select clms_nodal_ajs,clms_nodal_secu,clms_nodal_hr,clms_nodal_user,hod_functional_area,hod_man from department where hod_functional_area = '{_init_by}' or hod_man = '{_init_by}'"
            query = db.session.execute(query)
            DeptSchema = Department_schema(many=True)
            result = DeptSchema.dump(query)
            if result:
                result = list(set(map(operator.itemgetter('clms_nodal_ajs','clms_nodal_hr','clms_nodal_user','clms_nodal_secu','hod_man','hod_functional_area'), result)))[0]
                result = list(result)
                result.append(_init_by)
            else:
                result = [_init_by,_init_by]
                
            #result = list(set())
            # if form_search:
            #     #search_key = request_data["search_key"]
            #     fetchQuery = f"select * from cr_info WHERE unique_id ILIKE '{form_search}%'AND last_updated_by = '{_init_by}' ORDER BY unique_id, created_at DESC LIMIT 10 OFFSET {offset}"
            #     countQuery = f"SELECT COUNT(*) FROM (select * from cr_info WHERE unique_id ILIKE '{form_search}%'AND last_updated_by = '{_init_by}' ORDER BY unique_id, created_at DESC) as cnt"
            if search:
                #search_key = request_data["search_key"]
                fetchQuery = f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id FROM cr_info WHERE (form_heading ILIKE '%{search}%' OR unique_id ILIKE '%{search}%') AND last_updated_by IN {tuple(i for i in result)}  ORDER BY unique_id, created_at DESC "
                countQuery = f"SELECT COUNT(*) FROM (select * from cr_info WHERE (form_heading ILIKE '%{search}%' OR unique_id ILIKE '%{search}%') AND last_updated_by IN {tuple(i for i in result)} ORDER BY unique_id, created_at DESC) as cnt"
                # fetchQuery = f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id FROM cr_info WHERE (form_heading ILIKE '%{search}%' OR unique_id ILIKE '%{search}%') AND last_updated_by = '{_init_by}'  ORDER BY unique_id, created_at DESC "
                # countQuery = f"SELECT COUNT(*) FROM (select * from cr_info WHERE (form_heading ILIKE '%{search}%' OR unique_id ILIKE '%{search}%') AND last_updated_by = '{_init_by}' ORDER BY unique_id, created_at DESC) as cnt"
                data = db.session.execute(fetchQuery)
                CrInfoSchema = cr_info_schema(many=True)
                access_form = CrInfoSchema.dump(data)
                access_form = [a_dict["unique_id"] for a_dict in access_form]
                access_form.append(access_form[-1])
                if access_form:
                    fetchQuery2 =f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id,*  from cr_info where unique_id in {tuple(access_form)} ORDER BY unique_id, created_at DESC LIMIT 10 OFFSET {offset}"
                    #countQuery = f"SELECT COUNT(*) FROM (select * from cr_info where cr_info.id in {tuple(access_form)} and cr_info.form_status in ('{status}')) as cnt"
                    data2 = db.session.execute(fetchQuery2)
                    CrInfoSchema = cr_info_schema(many=True)
                    access_fm = CrInfoSchema.dump(data2)
            else:
                fetchQuery = f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id FROM cr_info WHERE last_updated_by IN {tuple(i for i in result)}  ORDER BY unique_id, created_at DESC "
                countQuery = f"SELECT COUNT(*) FROM (select * from cr_info WHERE last_updated_by IN {tuple(i for i in result)} ORDER BY unique_id, created_at DESC) as cnt"
                # fetchQuery = f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id FROM cr_info WHERE last_updated_by IN '{_init_by}'  ORDER BY unique_id, created_at DESC "
                # countQuery = f"SELECT COUNT(*) FROM (select * from cr_info WHERE last_updated_by = '{_init_by}' ORDER BY unique_id, created_at DESC) as cnt"
                data = db.session.execute(fetchQuery)
                CrInfoSchema = cr_info_schema(many=True)
                access_form = CrInfoSchema.dump(data)
                access_form = [a_dict["unique_id"] for a_dict in access_form]
                access_form.append(access_form[-1])
                if access_form:
                    fetchQuery2 =f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id,* from cr_info where unique_id in {tuple(access_form)} ORDER BY unique_id, created_at DESC LIMIT 10 OFFSET {offset}"
                    #countQuery = f"SELECT COUNT(*) FROM (select * from cr_info where cr_info.id in {tuple(access_form)} and cr_info.form_status in ('{status}')) as cnt"
                    data2 = db.session.execute(fetchQuery2)
                    CrInfoSchema = cr_info_schema(many=True)
                    access_fm = CrInfoSchema.dump(data2)

            # data = db.session.execute(fetchQuery)
            # CrInfoSchema = cr_info_schema(many=True)
            # access_form = CrInfoSchema.dump(data)

            access_count = db.session.execute(countQuery).scalar()
            
            # for each in access_form:
            #     for k,v in permit(each["cost_center"]).items():
            #         permit_.extend(v)
            #     each["view"] = True if _init_by  in permit_ else False

            response = {
                #"permission": Department.check_ROW_if_exists_in_Table(str(decoded_token["employee_id"])) if "employee_id" in decoded_token.keys() else False,
                "message": "CR Form fetched successfully",
                #"cr_forms": get_cr_forms,  # if permit_ else [],
                "submitted_forms": access_fm,
                #"access_form": sorted(submit_form, key=lambda k : k['created_at'], reverse=True),
                "count": len(access_form)
            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200
            
class CRForminitAccess(MethodView):
    @user_Access
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/view_cr_form.yaml', methods=['POST'])
    def post(self):
        try:
            token = request.headers.get('token')
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            # print(decoded_token)
            request_data = request.get_json(force=True)
            #access_form_page = request_data['access_form_page']
            #submitted_forms_page = request_data['submitted_forms_page']
            submit_form = list()
            query = cr_forms.query.filter(cr_forms.status == "active").order_by(cr_forms.created_at.desc()).all()
            CRFormSchema = cr_forms_schema(many=True)
            get_cr_forms = CRFormSchema.dump(query)
            _init_by = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"]

            response = {
                "permission": Department.check_ROW_if_exists_in_Table(str(decoded_token["employee_id"])) if "employee_id" in decoded_token.keys() else False,
                "message": "CR Form fetched successfully",
                "cr_forms": get_cr_forms,  # if permit_ else [],

            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200
            
# class CRForminit(MethodView):
#     @user_Access
#     @cross_origin(supports_credentials=True)
#     # @swag_from('apidocs/view_cr_form.yaml', methods=['POST'])
#     def post(self):
#         try:
#             token = request.headers.get('token')
#             decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
#             # print(decoded_token)
#             request_data = request.get_json(force=True)
#             access_form_page = request_data['access_form_page']
#             #submitted_forms_page = request_data['submitted_forms_page']
#             submit_form = list()
#             query = cr_forms.query.filter(cr_forms.status == "active").order_by(cr_forms.created_at.desc()).all()
#             CRFormSchema = cr_forms_schema(many=True)
#             get_cr_forms = CRFormSchema.dump(query)
#             _init_by = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"]
#             # if int(decoded_token["id"]) != 1:
#             #     designation_id = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["designation_id"]
#             #     designation = Designations.FetchDesignationDetails_By_ID(designation_id)["name"]
#             # query_2 = Cr_info.query.filter_by(init_by=_init_by).all() 
#             # CrInfoSchema = cr_info_schema(many=True)
#             # summitted_form = CrInfoSchema.dump(query_2)
#             access = list()
#             #submit_list = list()

#             #for _form_id in [each["id"] for each in get_cr_forms]:
                
#             query_3 = Cr_info.query.filter_by().order_by(Cr_info.created_at.desc()).all()
#             CrInfoSchema = cr_info_schema(many=True)
#             access_form = CrInfoSchema.dump(query_3)
#             form_id_list = list()
#             permit_ =[]
#             for each in access_form:
#                 if each["unique_id"] not in form_id_list:
#                     form_id_list.append(each["unique_id"])
#                     each["form_heading"]= form_heading_concat(each["unique_id"])
#                     each["form_slug"] = "Form"+each["unique_id"].split("_", 2)[1]
#                     print("permit", permit(each["cost_center"]))
#                     for k,v in permit(each["cost_center"]).items():
#                         permit_.extend(v)
#                     each["view"] = True if _init_by  in permit_ else False
#                     if each["status"] == "correction":
#                         each["edit"] = True if _init_by in \
#                                               finite_state_machine(each["state"], permit(each["cost_center"]))[
#                                                   "previous_list"] else False
                    
                    
                                                   
#                     else:
#                         each["edit"] = True \
#                             if _init_by in finite_state_machine(each["state"], permit(each["cost_center"]))[
#                             "next_list"] \
#                               and each["status"] != "correction" and each["status"] != "rejected" \
#                               and each["form_status"] != "onboard" else False

#                     print(each["edit"])
#                     #each["submission_date"]= each["created_at"]
#                     new_each = {**each}
#                     #access.append(each)
#                     access.append(new_each)
#                     # submit_form.append(new_each)
            
#             if "employee_id" in decoded_token.keys(): # ignore admin
#                 permit_ = Department.check_ROW_if_exists_in_Table(str(decoded_token["employee_id"]))
#             response = {
#                 "permission": Department.check_ROW_if_exists_in_Table(str(decoded_token["employee_id"])) if "employee_id" in decoded_token.keys() else False,
#                 "message": "CR Form fetched successfully",
#                 "cr_forms": get_cr_forms,  # if permit_ else [],
#                 # "submitted_forms": sorted(submit_form, key=lambda k : k['created_at'], reverse=True),
#                 # "submitted_forms_count":len(sorted(submit_form, key=lambda k : k['created_at'], reverse=True)),
#                 "access_form": sorted(access, key=lambda k : k['created_at'], reverse=True),
#                 "access_form_count":len(sorted(access, key=lambda k : k['created_at'], reverse=True))
#             }
#             return make_response(jsonify(response)), 200
#         except Exception as e:
#             import traceback
#             traceback.print_exc()
#             response = {"status": 'Error', "message": f'{str(e)}'}
#             print(response)
#             return make_response(jsonify(response)), 200
            
# class RECRForminit(MethodView):
#     @user_Access
#     @cross_origin(supports_credentials=True)
#     # @swag_from('apidocs/view_cr_form.yaml', methods=['POST'])
#     def post(self):
#         try:
#             token = request.headers.get('token')
#             decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
#             # print(decoded_token)
#             submit_form = list()
#             query = cr_forms.query.filter(cr_forms.status != "delete",Cr_info.form_state_status == 'release').order_by(cr_forms.created_at.desc()).all()
#             CRFormSchema = cr_forms_schema(many=True)
#             get_cr_forms = CRFormSchema.dump(query)
#             _init_by = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"]
#             if int(decoded_token["id"]) != 1:
#                 designation_id = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["designation_id"]
#                 designation = Designations.FetchDesignationDetails_By_ID(designation_id)["name"]
#             # query_2 = Cr_info.query.filter_by(init_by=_init_by).all()
#             # CrInfoSchema = cr_info_schema(many=True)
#             # summitted_form = CrInfoSchema.dump(query_2)
#             access = list()
#             submit_list = list()
#
#             for _form_id in [each["id"] for each in get_cr_forms]:
#
#                 query_3 = Cr_info.query.filter(Cr_info.form_id == str(_form_id),
#                                                Cr_info.form_state_status == 'release').order_by(
#                     Cr_info.created_at.desc()).all()
#                 CrInfoSchema = cr_info_schema(many=True)
#                 access_form = CrInfoSchema.dump(query_3)
#                 form_id_list = list()
#                 for each in access_form:
#                     form_state_status = [each["form_state_status"] for each in Cr_info.Fetch_cr_info(each["unique_id"] )]
#                     if each["unique_id"] not in form_id_list :
#                         form_id_list.append(each["unique_id"])
#                         each["form_heading"] = form_heading_concat(each["unique_id"])
#                         each["form_slug"] = "Form" + each["unique_id"].split("_", 2)[1]
#                         if each["form_state_status"] == "release":
#                             if cr_dd.get_user_demog_value_by_demog_id(each["unique_id"]):
#                                 _employee_id = cr_dd.get_user_demog_value_by_demog_id(each["unique_id"])
#                                 print(Users.FetchUSerDetails_By_clms_id(_employee_id[0]["d_value"]),"time to check")
#                                 if Users.FetchUSerDetails_By_clms_id(_employee_id[0]["d_value"])["vendor_id"] :
#                                     print("here_1")
#                                     each["view"] = False
#                                 elif form_state_status[0]!= "release":
#                                     each["view"] = False
#                                 else:
#                                     print("here_2",Users.FetchUSerDetails_By_clms_id(_employee_id[0]["d_value"])["vendor_id"])
#                                     each["view"] = True
#
#                             new_each = {**each}
#                             # access.append(each)
#                             access.append(new_each)
#                             # submit_form.append(new_each)
#
#             if "employee_id" in decoded_token.keys():  # ignore admin
#                 permit_ = Department.check_ROW_if_exists_in_Table(str(decoded_token["employee_id"]))
#             response = {
#                 "permission": Department.check_ROW_if_exists_in_Table(
#                     str(decoded_token["employee_id"])) if "employee_id" in decoded_token.keys() else False,
#                 "message": "Reinitiate CR Form fetched successfully",
#                 "cr_forms": get_cr_forms,  # if permit_ else [],
#                 "access_form": sorted(access, key=lambda k: k['created_at'], reverse=True)
#             }
#             return make_response(jsonify(response)), 200
#         except Exception as e:
#             import traceback
#             traceback.print_exc()
#             response = {"status": 'Error', "message": f'{str(e)}'}
#             print(response)
#             return make_response(jsonify(response)), 200

class RECRForminit(MethodView):
    @user_Access
    @cross_origin(supports_credentials=True)
    def post(self):
        try:
            token = request.headers.get('token')
            request_data = request.get_json(force=True)
            page_no = request_data['page_no']
            # form_search = request_data['form_search']
            search = request_data['search']
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            _init_by = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"]
            print("_init_by----------", _init_by)
            offset = int(10) * (int(page_no) - 1)
            access = list()
            permit_ = []
            _init_by = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"]
            query = f"select clms_nodal_ajs,clms_nodal_secu,clms_nodal_hr,clms_nodal_user,hod_functional_area,hod_man from department where hod_functional_area = '{_init_by}' or hod_man = '{_init_by}'"
            query = db.session.execute(query)
            DeptSchema = Department_schema(many=True)
            result = DeptSchema.dump(query)
            if result:
                result = list(set(map(
                    operator.itemgetter('clms_nodal_ajs', 'clms_nodal_secu', 'clms_nodal_hr', 'clms_nodal_user',
                                        'hod_man', 'hod_functional_area'), result)))[0]
                result = list(result)
                result.append(_init_by)
            else:
                result = [_init_by, _init_by]

            # result = list(set())
            # if form_search:
            #     #search_key = request_data["search_key"]
            #     fetchQuery = f"select * from cr_info WHERE unique_id ILIKE '{form_search}%'AND last_updated_by = '{_init_by}' ORDER BY unique_id, created_at DESC LIMIT 10 OFFSET {offset}"
            #     countQuery = f"SELECT COUNT(*) FROM (select * from cr_info WHERE unique_id ILIKE '{form_search}%'AND last_updated_by = '{_init_by}' ORDER BY unique_id, created_at DESC) as cnt"
            print("result------", result)
            if search:
                # search_key = request_data["search_key"]
                fetchQuery = f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id FROM cr_info WHERE (form_heading ILIKE '%{search}%' OR unique_id ILIKE '%{search}%') AND last_updated_by IN {tuple(i for i in result)} ORDER BY unique_id, created_at DESC "
                # countQuery = f"SELECT COUNT(*) FROM (select * from cr_info WHERE (form_heading ILIKE '%{search}%' OR unique_id ILIKE '%{search}%') AND last_updated_by IN {tuple(i for i in result)}  ORDER BY unique_id, created_at DESC) as cnt"
                # fetchQuery = f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id FROM cr_info WHERE (form_heading ILIKE '%{search}%' OR unique_id ILIKE '%{search}%') AND last_updated_by = '{_init_by}'  ORDER BY unique_id, created_at DESC "
                # countQuery = f"SELECT COUNT(*) FROM (select * from cr_info WHERE (form_heading ILIKE '%{search}%' OR unique_id ILIKE '%{search}%') AND last_updated_by = '{_init_by}' ORDER BY unique_id, created_at DESC) as cnt"
                data = db.session.execute(fetchQuery)
                CrInfoSchema = cr_info_schema(many=True)
                access_form = CrInfoSchema.dump(data)
                access_form = [a_dict["unique_id"] for a_dict in access_form]
                access_form.append(access_form[-1])
                if access_form:
                    fetchQuery2 = f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id,*  from cr_info where unique_id in {tuple(access_form)} AND form_status = 'release' ORDER BY unique_id, created_at DESC LIMIT 10 OFFSET {offset}"
                    countQuery = f"SELECT COUNT(*) FROM (select * from cr_info where unique_id in {tuple(access_form)} and form_status = 'release') as cnt"
                    data2 = db.session.execute(fetchQuery2)
                    CrInfoSchema = cr_info_schema(many=True)
                    access_fm = CrInfoSchema.dump(data2)
            else:
                fetchQuery = f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id FROM cr_info WHERE last_updated_by IN {tuple(i for i in result)} ORDER BY unique_id, created_at DESC "
                # countQuery = f"SELECT COUNT(*) FROM (select * from cr_info WHERE last_updated_by IN {tuple(i for i in result)}  ORDER BY unique_id, created_at DESC) as cnt"
                # fetchQuery = f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id FROM cr_info WHERE last_updated_by IN '{_init_by}'  ORDER BY unique_id, created_at DESC "
                # countQuery = f"SELECT COUNT(*) FROM (select * from cr_info WHERE last_updated_by = '{_init_by}' ORDER BY unique_id, created_at DESC) as cnt"
                data = db.session.execute(fetchQuery)
                CrInfoSchema = cr_info_schema(many=True)
                access_form = CrInfoSchema.dump(data)
                access_form = [a_dict["unique_id"] for a_dict in access_form]
                access_form.append(access_form[-1])
                if access_form:
                    fetchQuery2 = f"SELECT DISTINCT ON (cr_info.unique_id) cr_info.unique_id,* from cr_info where unique_id in {tuple(access_form)} AND form_status = 'release' ORDER BY unique_id, created_at DESC LIMIT 10 OFFSET {offset}"
                    countQuery = f"SELECT COUNT(*) FROM (select * from cr_info where unique_id in {tuple(access_form)} and form_status = 'release') as cnt"
                    data2 = db.session.execute(fetchQuery2)
                    CrInfoSchema = cr_info_schema(many=True)
                    access_fm = CrInfoSchema.dump(data2)

            # data = db.session.execute(fetchQuery)
            # CrInfoSchema = cr_info_schema(many=True)
            # access_form = CrInfoSchema.dump(data)

            access_count = db.session.execute(countQuery).scalar()

            response = {
                # "permission": Department.check_ROW_if_exists_in_Table(str(decoded_token["employee_id"])) if "employee_id" in decoded_token.keys() else False,
                "message": "CR Form release fetched successfully",
                # "cr_forms": get_cr_forms,  # if permit_ else [],
                "submitted_forms": access_fm,
                # "access_form": sorted(submit_form, key=lambda k : k['created_at'], reverse=True),
                "count": access_count
            }
            return make_response(jsonify(response)), 200
        except IndexError as e:
            import traceback
            traceback.print_exc()
            response = {
                # "permission": Department.check_ROW_if_exists_in_Table(str(decoded_token["employee_id"])) if "employee_id" in decoded_token.keys() else False,
                "message": "CR Form release fetched successfully",
                # "cr_forms": get_cr_forms,  # if permit_ else [],
                "submitted_forms": [],
                # "access_form": sorted(submit_form, key=lambda k : k['created_at'], reverse=True),
                "count": 0
            }
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200
            
class Forminit(MethodView):
    @user_Access
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/view_cr_form.yaml', methods=['POST'])
    def post(self):
        try:
            token = request.headers.get('token')
            request_data = request.get_json(force=True)
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            _init_by = Users.FetchUSerDetails_By_ID(int(decoded_token["id"]))["employee_id"]
            crgroups = list()
            dm_list = list()
            cr_form = cr_forms.query.filter(cr_forms.form_slug == request_data['slug']). \
                order_by(cr_forms.updated_at.desc()).first()
            CRFormSchema = cr_forms_schema()
            output_form = CRFormSchema.dump(cr_form)
            
            # query = po_master.query.all()
            # CrFormGroupSchema = po_master_schema(many=True)
            # output_po = CrFormGroupSchema.dump(query)
            output_po = list()

            query_dept = Department.query.filter(
            (Department.clms_nodal_user == _init_by) | (Department.hod_man == _init_by) | (
                        Department.hod_functional_area == _init_by)).all()
            DeptSchema = Department_schema(many=True)
            output_dept = DeptSchema.dump(query_dept)
            if output_form.get("id"):
                crgroup = cr_form_groups.get_cr_form_by_formid(output_form.get("id"))
                for group in crgroup:
                    # print(group)
                    cr_group_ = cr_groups.Fetch_cr_group_by_groupid(int(group))
                    cr_demong_group = cr_demog_groups.Fetch_cr_demog_group(cr_group_["id"])
                    for demog in cr_demong_group:
                        Demong_master = dm.get_demog_by_id(int(demog))
                        dm_list.append(Demong_master)
                    # print(dm_list)
                    cr_group_["demog_masters"] = dm_list
                    dm_list = []
                    crgroups.append(cr_group_)
            response = {
                "Dept_master": output_dept,
                "message": "CR Form fetched successfully",
                "po_master": output_po if output_po else [],
                "formDetails": output_form if output_form else [],
                "formGroup": sorted(crgroups, key=lambda d: d['name']) if crgroups else [] if crgroups else []
            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200

class UpdateCrFormStatus(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/update_cr_form_status.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            _id = request_data["id"]
            status = request_data['status']
            cr_forms.Change_Status(_id, status)
            response = {
                "status": "success",
                "message": "CR Form status updated successfully"}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class GetCrForm(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/get_cr_form.yaml', methods=['GET'])
    def get(self, page_no):
        try:
            
            query = cr_forms.query.filter(cr_forms.status != "inactive").order_by(cr_forms.form_name).all()
            CRFormSchema = cr_forms_schema(many=True)
            output = CRFormSchema.dump(query)
            response = {
                "status": "success",
                "message": "CR Form listing fetched successfully",
                "CRFormList": Paginate(output, page_no) if page_no != "all" else output,
                "SearchCount": len(output)

            }
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class GetCrFormBySlug(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/get_cr_form_by_slug.yaml', methods=['GET'])
    def get(self, slug):
        try:
            print(str(slug))
            crgroups = list()
            dm_list = list()
            cr_form = cr_forms.query.filter(cr_forms.form_slug == slug).order_by(cr_forms.form_name).first()
            CRFormSchema = cr_forms_schema()
            output = CRFormSchema.dump(cr_form)
            if output.get("id") :
                crgroup = cr_form_groups.get_cr_form_by_formid(output.get("id"))
                for group in crgroup:
                    # print(group)
                    cr_group_ = cr_groups.Fetch_cr_group_by_groupid(int(group))
                    cr_demong_group = cr_demog_groups.Fetch_cr_demog_group(cr_group_["id"])
                    # print("cr_demong_group", cr_demong_group)
                    for demog in cr_demong_group:
                        Demong_master = dm.get_demog_by_id(int(demog))
                        dm_list.append(Demong_master)
                    # print(dm_list)
                    cr_group_["demog_masters"] = dm_list
                    dm_list = []
                    crgroups.append(cr_group_)

                print(crgroups)
                response = {
                    "status": "success",
                    "message": "CR Form fetched successfully",
                    "formDetails": output,
                    "formGroup": crgroups
                }
                print(response)
                return make_response(jsonify(response)), 200
            else:
                response = {
                    "status": "error",
                    "message": "Can't fetched CR Form successfully"
                               " Slug not found",
                    "formDetails": [],
                    "formGroup": []
                }
                print(response)
                return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class CreateCRFormGroup(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/add_cr_form_group.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            form_id = request_data["form_id"]
            group_id = request_data["group_id"]  # list
            status = request_data['status']
            cr_form_group = cr_form_groups.query.filter_by(form_id=str(form_id)) \
                .with_entities(cr_form_groups.id).all()
            CRFormGroupSchema = cr_form_groups_schema(many=True)
            output = CRFormGroupSchema.dump(cr_form_group)
            output = [each["id"] for each in output]
            for _each in output:
                cr_form_groups.query.filter_by(id=int(_each)).delete()
                db.session.commit()
            for each in group_id:
                if cr_form_groups.check_cr_form_if_exists_in_group(form_id, each):
                    cr_form_groups.Add_cr_form_group(form_id, each, status)
            response = {
                "status": "success",
                "message": "CR form group updated successfully"}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class UpdateCrFormGroupStatus(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/update_cr_form_group_status.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            _id = request_data["id"]
            status = request_data['status']
            cr_form_groups.Change_Status(_id, status)
            response = {
                "status": "success",
                "message": "CR Form group status updated successfully"}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class UpdateCrFormGroup(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/update_cr_form_group.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            _id = request_data["id"]
            form_id = request_data["form_id"]
            group_id = request_data["group_id"]
            cr_form_groups.Update_cr_form_groups(_id, form_id, group_id)
            response = {
                "status": "success",
                "message": "CR Form group updated successfully"}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class GetCrFormGroup(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/get_cr_form_group.yaml', methods=['GET'])
    def get(self, page_no):
        try:
            cr_form_group = cr_form_groups.query.filter(cr_form_groups.status != "delete") \
                .order_by(cr_form_groups.updated_at.desc()).all()
            CRFormGroupSchema = cr_form_groups_schema(many=True)
            output = CRFormGroupSchema.dump(cr_form_group)
            response = {
                "status": "success",
                "message": "CR Form group fetched successfully",
                "CrFormGroupList": Paginate(output, page_no) if page_no != "all" else output,
                "SearchCount": len(output)}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class CreatePOMaster(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/add_po_master.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            po_date = request_data['po_date']
            po_title = request_data.get('po_title', None)
            supplier_code = request_data.get('supplier_code', None)
            assign_date = request_data.get('assign_date', None)
            expiry = request_data.get('expiry', None)
            po_number = request_data['po_number']
            status = request_data['status']
            po_details = request_data.get('po_details', None)
            if po_master.check_cr_form_if_exists_in_po(po_number):
                po_master.Add_po_master(po_number, po_date, po_title, po_details, supplier_code, assign_date, expiry,
                                        status)
                response = {
                    "status": "success",
                    "message": "PO Master created successfully"}
            else:
                response = {
                    "status": "Error",
                    "message": "PO number already exist"}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class UpdatePOMasterStatus(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/update_po_master_status.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            _id = request_data["id"]
            status = request_data['status']
            po_master.Change_Status(_id, status)
            response = {
                "status": "success",
                "message": "PO Master status updated successfully"}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class UpdatePOMaster(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/update_po_master.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            _id = request_data["id"]
            # po_date = request_data['po_date']
            po_title = request_data['po_title']
            # supplier_code = request_data['supplier_code']
            # assign_date = request_data['assign_date']
            # expiry = request_data['expiry']
            # po_number = request_data['po_number']
            po_details = request_data['po_details']
            po_master.Update_po_master(_id, po_title, po_details)
            response = {
                "status": "success",
                "message": "PO Master updated successfully"}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class GetPo(MethodView):
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/add_po_master.yaml', methods=['POST'])
    def post(self):
        try:
            result = list()
            request_data = request.get_json(force=True)
            search = request_data["search"]
            page_no = "all"
            output = []
            if search:
                if str.isdigit(search):
                    search_query = f"SELECT * FROM ft_sap_order WHERE po_number ilike '%{search}%' FETCH FIRST 20 ROW " \
                                   f"ONLY "
                else:
                    search_query = f"SELECT * FROM ft_sap_order WHERE vendor_name ilike '%{search}%' FETCH FIRST 20 " \
                                   f"ROW ONLY "
                data = db.session.execute(search_query)
                CrFormGroupSchema = ft_sap_order_schema(many=True)
                output = CrFormGroupSchema.dump(data)
                for each in output:
                    if po_master.check_cr_form_if_exists_in_po(each["po_number"]):
                        print(each["po_number"])
                        result.append(each)

            response = {
                "status": "success",
                "message": "PO fetched successfully",
                "output":  Paginate(output, page_no) if page_no != "all" else output,
                "All_Search_count": len(result)
            }
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200
            
            
class GetPoForm(MethodView):
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/add_po_master.yaml', methods=['POST'])
    def post(self):
        try:
            result = list()
            output2 = list()
            request_data = request.get_json(force=True)
            slug = request_data["slug"]
            searchKey = request_data["searchKey"]
            if searchKey:
                if str.isdigit(searchKey):
                    search_query = f"SELECT * FROM po_master WHERE expiry > NOW() AND status != 'delete' AND po_number::text like '%{searchKey}%' LIMIT 10"
                else:
                    search_query = f"SELECT * FROM po_master WHERE expiry > NOW() AND status != 'delete' AND po_title ilike '%{searchKey}%' LIMIT 10"

                # else:
                #     search_query = f"SELECT * FROM po_master WHERE expiry > NOW()"

                data = db.session.execute(search_query)
                PoMasterSchema = po_master_schema(many=True)
                output = PoMasterSchema.dump(data)
                if slug == "FormB2":
                    for each in output:
                        if Cr_info.check_cr_form_if_exists_in_po(each["po_number"]):
                            search = each["po_number"]
                            search_query = f"SELECT * FROM ft_sap_order WHERE po_number = '{search}'"
                            data1 = db.session.execute(search_query)
                            CrFormGroupSchema = ft_sap_order_schema(many=True)
                            output2 = CrFormGroupSchema.dump(data1)
                            if output2:
                                result.append(output2[-1])
                else:
                    for each_ in output:
                        if Cr_info.check_cr_form_if_exists_in_po(each_["po_number"]) is False:
                            search = each_["po_number"]
                            search_query = f"SELECT * FROM ft_sap_order WHERE po_number = '{search}'"
                            data1 = db.session.execute(search_query)
                            CrFormGroupSchema = ft_sap_order_schema(many=True)
                            output2 = CrFormGroupSchema.dump(data1)
                            if output2:
                                result.append(output2[-1])

            response = {
                "status": "success",
                "message": "Fetch PO Master successfully",
                "result": result
            }

            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200
            
            
class GetPoMaster(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/get_po_master.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            page_no = request_data["page_no"]
            search = request_data["search"]
            if page_no != "all":
                offset = int(10) * (int(page_no) - 1)
            if search:
                if str.isdigit(search):
                    search_query = f"SELECT * FROM po_master WHERE status != 'delete' AND  po_number::text like '%{search}%'" \
                                   f" OR po_title ilike'%{search}%' LIMIT 10 OFFSET {offset}"
                    search_query2 = f"SELECT * FROM po_master WHERE status != 'delete' AND  po_number::text like '%{search}%'" \
                                   f" OR po_title ilike'%{search}%' "
                else:
                    search_query = f"SELECT * FROM po_master WHERE status != 'delete' " \
                                   f" AND po_title ilike '%{search}%' LIMIT 10 OFFSET {offset}"
                    search_query2 = f"SELECT * FROM po_master WHERE status != 'delete' " \
                                   f" AND po_title ilike '%{search}%' "
                data = db.session.execute(search_query)
                POSchema = po_master_schema(many=True)
                output = POSchema.dump(data)
                data2 = db.session.execute(search_query2)
                POSchema = po_master_schema(many=True)
                output2 = POSchema.dump(data2)
            else:
                search_query = f"SELECT * FROM po_master WHERE status != 'delete' " \
                                   f" LIMIT 10 OFFSET {offset}"
                search_query2 = f"SELECT * FROM po_master WHERE status != 'delete' " 
                data = db.session.execute(search_query)
                POSchema = po_master_schema(many=True)
                output = POSchema.dump(data)
                data2 = db.session.execute(search_query2)
                POSchema = po_master_schema(many=True)
                output2 = POSchema.dump(data2)
            response = {
                "status": "success",
                "message": "PO Master fetched successfully",
                "POMasterList":output,
                "SearchCount": len(output2) 

            }
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200

class CreateVendors(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/add_vendors.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            vd_code = request_data['vd_code']
            vd_scrum_id = request_data['vd_scrum_id']
            is_deleted = request_data['is_deleted']
            status = request_data['status']
            name = request_data["name"]
            if vendors.check_cr_form_if_exists_in_vendor(vd_code):
                vendors.Add_vendors(name, vd_code, vd_scrum_id, is_deleted, status)
                response = {
                    "status": "success",
                    "message": "New Vendor added successfully"}
                print(response)
            else:
                response = {
                    "status": "success",
                    "message": "Vendor already exists"}
                print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200

class UpdateVendorStatus(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/update_vendor_status.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            _id = request_data["id"]
            status = request_data['status']
            vendors.Change_Status(_id, status)
            response = {
                "status": "success",
                "message": "Vendor status updated successfully"}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class UpdateVendor(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/update_vendor.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            vd_code = request_data['vd_code']
            vd_scrum_id = request_data['vd_scrum_id']
            is_deleted = request_data['is_deleted']
            _id = request_data['id']
            name = request_data["name"]
            vendors.Update_vendors(_id, name, vd_code, vd_scrum_id, is_deleted)
            response = {
                "status": "success",
                "message": "Vendor updated successfully"}
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class GetVendor(MethodView):
    @cross_origin(supports_credentials=True)
    @swag_from('apidocs/get_vendor.yaml', methods=['GET'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            search = request_data['search']
            page_no = request_data['page_no']
            if page_no != "all":
                offset = int(10) * (int(page_no) - 1)
            #search_query = f"SELECT * FROM vendors LIMIT 10 OFFSET {offset}"
            print(search)
            if search != "all" and search:
                # if search.isalnum():
                #     print("alpha")
                search_query = f"SELECT * FROM vendors WHERE vd_code ilike '%{search}%' OR name ilike '%{search}%' LIMIT 10 OFFSET {offset} "
                search_query2 = f"SELECT * FROM vendors WHERE vd_code ilike '%{search}%' OR name ilike '%{search}%' "
                # elif search.isalpha():
                #     print("not alpha")
                #     search_query = f"SELECT * FROM vendors WHERE name ilike '%{search}%'LIMIT 10 OFFSET {offset}"
                #     print(search_query)

                data = db.session.execute(search_query)
                vendorsSchema = vendors_schema(many=True)
                output = vendorsSchema.dump(data)
                data2 = db.session.execute(search_query2)
                vendorsSchema = vendors_schema(many=True)
                output2 = vendorsSchema.dump(data2)
            elif search == "all":
                query = vendors.query.filter(vendors.status != "delete").order_by(vendors.updated_at.desc()).all()
                VendorSchema = vendors_schema(many=True)
                output = VendorSchema.dump(query)
            else:
                # if search.isalnum():
                #     print("alpha")
                #     search_query = f"SELECT * FROM vendors  LIMIT 10 OFFSET {offset} "
                # elif search.isalpha():
                #     print("not alpha")
                search_query = f"SELECT * FROM vendors LIMIT 10 OFFSET {offset}"
                search_query2 = f"SELECT * FROM vendors"
                print(search_query)

                data = db.session.execute(search_query)
                vendorsSchema = vendors_schema(many=True)
                output = vendorsSchema.dump(data)
                data2 = db.session.execute(search_query2)
                vendorsSchema = vendors_schema(many=True)
                output2 = vendorsSchema.dump(data2)
                
            # for each in output:
            #     each["Labour_onboarded"] = Users.FetchUSerDetails_By_vendor_id(each["vd_code"])
            response = {
                "status": "success",
                "message": "Vendor list fetched successfully",
                "VendorList": output,
                "SearchCount": len(output) if search == "all"  else len(output2)
            }
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200
            
class GetDemogValueById(MethodView):
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/get_vendor.yaml', methods=['GET'])
    def post(self):
        try:
            result = {}
            request_data = request.get_json(force=True)
            unique_id = request_data.get("unique_id")
            dmog_code = request_data.get("demog_code")
            new_list = []
            for each in dmog_code:
                print(cr_dd.get_demog_value_by_demog_id(unique_id, each),"demong_value",each)
                if not cr_dd.get_demog_value_by_demog_id(unique_id, each):
                    pass
                else:
                    new_list.append({"key": each, "value": cr_dd.get_demog_value_by_demog_id(unique_id, each)["d_value"]})
            result["value"] = new_list
            result["form_type"] = unique_id.split("_", 2)[1]
            response = {
                "status": "success",
                "message": "Get Dmong value by Dmong ID",
                "result": result
            }
            print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200

class GetOnboardVendor(MethodView):
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/get_vendor.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            page_no = request_data.get('page_no',"all")
            vendorcode_search = request_data.get('vendorcode_search')
            vendorname_search = request_data.get('vendorname_search')
            po_search = request_data.get('po_search')
            uniqueid_search = request_data.get('uniqueid_search')
            #if page_no != "all":
            offset = int(10) * (int(page_no) - 1)
            onboard_list = list()
            if vendorcode_search:
                search_query = f"SELECT cr_info.yard_no,cr_info.unit,cr_info.dept,cr_info.po_number,cr_info.unique_id,cr_info.form_status, " \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_max_persons_allowed'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS Labour_limit," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_company_name'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS name," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_vendor_code'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto  THEN cr_dd.d_value "\
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS vd_code " \
                                f"FROM cr_info " \
                                f"RIGHT JOIN (select * from cr_dd where cr_dd.d_value ilike '%{vendorcode_search}%' and dcode = 'vd_vendor_code') cr_dd ON cr_info.unique_id = cr_dd.unique_id " \
                                f"WHERE cr_info.form_id = '1' " \
                                f"AND cr_info.form_status = 'onboard'" \
                                f"GROUP BY cr_info.yard_no," \
                                f"cr_info.unit," \
                                f"cr_info.dept," \
                                f"cr_info.po_number," \
                                f"cr_info.unique_id," \
                                f"cr_info.form_status LIMIT 10 OFFSET {offset}"
                data = db.session.execute(search_query)
                search_query2 = f"select count(*) from (SELECT cr_info.yard_no,cr_info.unit,cr_info.dept,cr_info.po_number,cr_info.unique_id,cr_info.form_status, " \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_max_persons_allowed'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS Labour_limit," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_company_name'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS name," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_vendor_code'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto  THEN cr_dd.d_value "\
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS vd_code " \
                                f"FROM cr_info " \
                                f"RIGHT JOIN (select * from cr_dd where cr_dd.d_value ilike '%{vendorcode_search}%' and dcode = 'vd_vendor_code') cr_dd ON cr_info.unique_id = cr_dd.unique_id " \
                                f"WHERE cr_info.form_id = '1' " \
                                f"AND cr_info.form_status = 'onboard'" \
                                f"GROUP BY cr_info.yard_no," \
                                f"cr_info.unit," \
                                f"cr_info.dept," \
                                f"cr_info.po_number," \
                                f"cr_info.unique_id," \
                                f"cr_info.form_status) as total_count "
                data2 = db.session.execute(search_query2).scalar()
            elif vendorname_search:
                search_query = f"SELECT cr_info.yard_no,cr_info.unit,cr_info.dept,cr_info.po_number,cr_info.unique_id,cr_info.form_status, " \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_max_persons_allowed'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS Labour_limit," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_company_name'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS name," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_vendor_code'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto  THEN cr_dd.d_value "\
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS vd_code " \
                                f"FROM cr_info " \
                                f"RIGHT JOIN (select * from cr_dd where cr_dd.d_value ilike '%{vendorname_search}%' and dcode = 'vd_company_name') cr_dd ON cr_info.unique_id = cr_dd.unique_id " \
                                f"WHERE cr_info.form_id = '1' " \
                                f"AND cr_info.form_status = 'onboard'" \
                                f"GROUP BY cr_info.yard_no," \
                                f"cr_info.unit," \
                                f"cr_info.dept," \
                                f"cr_info.po_number," \
                                f"cr_info.unique_id," \
                                f"cr_info.form_status LIMIT 10 OFFSET {offset}"
                data = db.session.execute(search_query)
                search_query2 = f"select count(*) from (SELECT cr_info.yard_no,cr_info.unit,cr_info.dept,cr_info.po_number,cr_info.unique_id,cr_info.form_status, " \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_max_persons_allowed'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS Labour_limit," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_company_name'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS name," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_vendor_code'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto  THEN cr_dd.d_value "\
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS vd_code " \
                                f"FROM cr_info " \
                                f"RIGHT JOIN (select * from cr_dd where cr_dd.d_value ilike '%{vendorname_search}%' and dcode = 'vd_company_name') cr_dd ON cr_info.unique_id = cr_dd.unique_id " \
                                f"WHERE cr_info.form_id = '1' " \
                                f"AND cr_info.form_status = 'onboard'" \
                                f"GROUP BY cr_info.yard_no," \
                                f"cr_info.unit," \
                                f"cr_info.dept," \
                                f"cr_info.po_number," \
                                f"cr_info.unique_id," \
                                f"cr_info.form_status) as total_count "
                data2 = db.session.execute(search_query2).scalar()
            elif po_search:
                search_query = f"SELECT cr_info.yard_no,cr_info.unit,cr_info.dept,cr_info.po_number,cr_info.unique_id,cr_info.form_status, " \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_max_persons_allowed'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS Labour_limit," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_company_name'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS name," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_vendor_code'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto  THEN cr_dd.d_value "\
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS vd_code " \
                                f"FROM cr_info " \
                                f"RIGHT JOIN  cr_dd ON cr_info.unique_id = cr_dd.unique_id " \
                                f"WHERE cr_info.form_id = '1' " \
                                f"AND cr_info.form_status = 'onboard' AND cr_info.po_number::text ilike '%{po_search}%'" \
                                f"GROUP BY cr_info.yard_no," \
                                f"cr_info.unit," \
                                f"cr_info.dept," \
                                f"cr_info.po_number," \
                                f"cr_info.unique_id," \
                                f"cr_info.form_status LIMIT 10 OFFSET {offset}"
                data = db.session.execute(search_query)
                search_query2 = f"select count(*) from (SELECT cr_info.yard_no,cr_info.unit,cr_info.dept,cr_info.po_number,cr_info.unique_id,cr_info.form_status, " \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_max_persons_allowed'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS Labour_limit," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_company_name'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS name," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_vendor_code'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto  THEN cr_dd.d_value "\
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS vd_code " \
                                f"FROM cr_info " \
                                f"RIGHT JOIN  cr_dd ON cr_info.unique_id = cr_dd.unique_id " \
                                f"WHERE cr_info.form_id = '1' " \
                                f"AND cr_info.form_status = 'onboard' AND cr_info.po_number::text ilike '%{po_search}%'" \
                                f"GROUP BY cr_info.yard_no," \
                                f"cr_info.unit," \
                                f"cr_info.dept," \
                                f"cr_info.po_number," \
                                f"cr_info.unique_id," \
                                f"cr_info.form_status) as total_count "
                data2 = db.session.execute(search_query2).scalar()
            elif uniqueid_search:
                print("unique")
                search_query = f"SELECT cr_info.yard_no,cr_info.unit,cr_info.dept,cr_info.po_number,cr_info.unique_id,cr_info.form_status, " \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_max_persons_allowed'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS Labour_limit," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_company_name'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS name," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_vendor_code'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto  THEN cr_dd.d_value "\
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS vd_code " \
                                f"FROM cr_info " \
                                f"RIGHT JOIN  cr_dd ON cr_info.unique_id = cr_dd.unique_id " \
                                f"WHERE cr_info.form_id = '1' " \
                                f"AND cr_info.form_status = 'onboard' AND cr_info.unique_id::text ilike '%{uniqueid_search}%'" \
                                f"GROUP BY cr_info.yard_no," \
                                f"cr_info.unit," \
                                f"cr_info.dept," \
                                f"cr_info.po_number," \
                                f"cr_info.unique_id," \
                                f"cr_info.form_status LIMIT 10 OFFSET {offset}"
                print(search_query)
                data = db.session.execute(search_query)
                search_query2 = f"select count(*) from (SELECT cr_info.yard_no,cr_info.unit,cr_info.dept,cr_info.po_number,cr_info.unique_id,cr_info.form_status, " \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_max_persons_allowed'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS Labour_limit," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_company_name'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS name," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_vendor_code'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto  THEN cr_dd.d_value "\
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS vd_code " \
                                f"FROM cr_info " \
                                f"RIGHT JOIN  cr_dd ON cr_info.unique_id = cr_dd.unique_id " \
                                f"WHERE cr_info.form_id = '1' " \
                                f"AND cr_info.form_status = 'onboard' AND cr_info.unique_id::text  ilike '%{uniqueid_search}%'" \
                                f"GROUP BY cr_info.yard_no," \
                                f"cr_info.unit," \
                                f"cr_info.dept," \
                                f"cr_info.po_number," \
                                f"cr_info.unique_id," \
                                f"cr_info.form_status) as total_count "
                data2 = db.session.execute(search_query2).scalar()
            else:
                search_query = f"SELECT cr_info.yard_no,cr_info.unit,cr_info.dept,cr_info.po_number,cr_info.unique_id,cr_info.form_status, " \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_max_persons_allowed'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS Labour_limit," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_company_name'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS name," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_vendor_code'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto  THEN cr_dd.d_value "\
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS vd_code " \
                                f"FROM cr_info " \
                                f"RIGHT JOIN cr_dd ON cr_info.unique_id = cr_dd.unique_id " \
                                f"WHERE cr_info.form_id = '1' " \
                                f"AND cr_info.form_status = 'onboard'" \
                                f"GROUP BY cr_info.yard_no," \
                                f"cr_info.unit," \
                                f"cr_info.dept," \
                                f"cr_info.po_number," \
                                f"cr_info.unique_id," \
                                f"cr_info.form_status LIMIT 10 OFFSET {offset}"
                data = db.session.execute(search_query)
                search_query2 = f"select count(*) from (SELECT cr_info.yard_no,cr_info.unit,cr_info.dept,cr_info.po_number,cr_info.unique_id,cr_info.form_status, " \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_max_persons_allowed'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS Labour_limit," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_company_name'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto THEN cr_dd.d_value " \
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS name," \
                                f"max(" \
                                f"CASE " \
                                f"WHEN cr_dd.dcode::text = 'vd_vendor_code'::text AND CURRENT_DATE >= cr_dd.efrom AND CURRENT_DATE <= cr_dd.eto  THEN cr_dd.d_value "\
                                f"ELSE NULL::character varying " \
                                f"END::text" \
                                f") AS vd_code " \
                                f"FROM cr_info " \
                                f"RIGHT JOIN cr_dd ON cr_info.unique_id = cr_dd.unique_id " \
                                f"WHERE cr_info.form_id = '1' " \
                                f"AND cr_info.form_status = 'onboard'" \
                                f"GROUP BY cr_info.yard_no," \
                                f"cr_info.unit," \
                                f"cr_info.dept," \
                                f"cr_info.po_number," \
                                f"cr_info.unique_id," \
                                f"cr_info.form_status) as total_count "
                data2 = db.session.execute(search_query2).scalar()

            
            #print(data[0])
            for each in data:
                print(each,"gggggggggggggggg")
                output2 = dict()
                # if po_master.Fetch_po_expiry_with_po_number(each[3])["expiry"]< str(datetime.now().date()):
                #     continue
                if data2 != 0:
                    print(data2,"here ----------",each)
                    output2["yard_no"] = each[0]
                    output2["unit"] = each[1]
                    output2["dept"] = each[2]
                    output2["po_number"] = each[3]
                    output2["unique_id"] = each[4]
                    output2["Labour_limit"] = each[6] if each[6] else cr_dd.get_demog_value_by_demog_id(each[4], "vd_max_persons_allowed")["d_value"]
                    output2["name"] = each[7] if each[7] else cr_dd.get_demog_value_by_demog_id(each[4], "vd_company_name")["d_value"]
                    output2["vd_code"] = each[8] if  each[8] else cr_dd.get_demog_value_by_demog_id(each[4], "vd_vendor_code")["d_value"]
                    output2["Labour_onboarded"] = labour_onboard_count(each[4])
                    onboard_list.append(output2)

            response = {
                "status": "success",
                "message": "Vendor Onboard list fetched successfully",
                "VendorList": onboard_list,
                "SearchCount": data2
            }
            #print(response)
            return make_response(jsonify(response)), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200
            
class user_verification(MethodView):
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/update_vendor.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            token = request_data['token']
            cost_center = request_data['cost_center']
            decoded_token = jwt.decode(token, current_app.config['USER_SECRET_KEY'], algorithms=['HS256'])
            init_by = Users.FetchUSerDetails_By_ID(decoded_token["id"])["employee_id"]
            permit_ = permit(cost_center)
            if init_by in permit_["clms_nodal_user"]:
                response = {
                    "status": "success",
                    "permit": True,
                    "user": init_by
                }
                
            else:
                return jsonify({"AUTH ERROR": "USER AUTHORISATION REQUIRED"}), 401
            
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200

class user_heading(MethodView):
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/update_vendor.yaml', methods=['POST'])
    def post(self):
        try:
            search_query = f"SELECT * FROM cr_info where form_heading is null"
            query = db.session.execute(search_query)
            CrInfoSchema = cr_info_schema(many=True)
            result = CrInfoSchema.dump(query)
            for each in result:
                #print("#############################")
                #print(each.get("unique_id"))
                Cr_info.query.filter_by(unique_id=each.get("unique_id")).update({
                Cr_info.form_heading: form_heading_concat(each.get("unique_id")),
                    })
                db.session.flush()
                db.session.commit()
            #labour_onboard_count(CR_B1_100225)
            #unique = "CR_B1_100225"

            response = {
                "status": "success",
                "data" :[]

            }
                
        
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class find_attachment_from_unique_id(MethodView):
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/update_vendor.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            unique_id = request_data['unique_id']
            result = list()

            code = unique_id.split("_", 2)[1]
            if code == "B1":
                the_dir = '/var/www/html/grse1/grse1/scan/b1'
                #the_dir = 'scan/b1'
                download_url = 'http://10.181.111.60/scan/b1/'
                search = cr_dd.get_demog_value_by_demog_id(unique_id, "vd_po").get("d_value", None)
                pass
            elif code == "B2":
                the_dir = '/var/www/html/grse1/grse1/scan/b2'
                #the_dir = 'scan/b2'
                download_url = 'http://10.181.111.60/scan/b2/'
                search = cr_dd.get_demog_value_by_demog_id(unique_id, "cl_aadhaar").get("d_value", None)
                pass
            fileNames = [fileName for fileName in os.listdir(the_dir) if fileName.startswith(search)]
            if fileNames:
                for each in fileNames:
                    result.append({"filename": each, "file_path": download_url + each})

            response = {
                "status": "success",
                "data": result,
                "count": len(result)

            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200


class find_attachment_with_page(MethodView):
    @cross_origin(supports_credentials=True)
    # @swag_from('apidocs/update_vendor.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            page_no = request_data['page_no']
            result = list()
            the_dir = '/var/www/html/grse1/grse1/mis'
            #the_dir = 'mis'
            download_url = 'http://10.181.111.60/mis/'
            fileNames = [fileName for fileName in os.listdir(the_dir)]
            if fileNames:
                for each in Paginate(fileNames, page_no, page_size=20):
                    result.append({"filename": each, "file_path": download_url + each})
            response = {
                "status": "success",
                "data": result,
                "count": len(fileNames)

            }

            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"status": 'Error', "message": f'{str(e)}'}
            print(response)
            return make_response(jsonify(response)), 200

# # # Creating View Function/Resources
CreateCRForm = CreateCRForm.as_view("CreateCRForm")
CreateCRForminit = CreateCRForminit.as_view("CreateCRForminit")
ViewCRForm = ViewCRForm.as_view("ViewCRForm")
CreateCRFormGroup = CreateCRFormGroup.as_view("CreateCRFormGroup")
UpdateCrFormGroupStatus = UpdateCrFormGroupStatus.as_view("UpdateCrFormGroupStatus")
UpdateCrFormGroup = UpdateCrFormGroup.as_view("UpdateCrFormGroup")
GetCrFormGroup = GetCrFormGroup.as_view("GetCrFormGroup")
UpdateCrFormStatus = UpdateCrFormStatus.as_view("UpdateCrFormStatus")
GetCrFormBySlug = GetCrFormBySlug.as_view("GetCrFormBySlug")
GetCrForm = GetCrForm.as_view("GetCrForm")
CreatePOMaster = CreatePOMaster.as_view("CreatePOMaster")
UpdatePOMasterStatus = UpdatePOMasterStatus.as_view("UpdatePOMasterStatus")
UpdatePOMaster = UpdatePOMaster.as_view("UpdatePOMaster")
GetPoMaster = GetPoMaster.as_view("GetPoMaster")
CreateVendors = CreateVendors.as_view("CreateVendors")
UpdateVendorStatus = UpdateVendorStatus.as_view("UpdateVendorStatus")
UpdateVendor = UpdateVendor.as_view("UpdateVendor")
GetVendor = GetVendor.as_view("GetVendor")
CRForminit = CRForminit.as_view("CRForminit")
RECRForminit = RECRForminit.as_view("RECRForminit")
Forminit = Forminit.as_view("Forminit")
GetDemogValueById = GetDemogValueById.as_view("GetDemogValueById")
GetOnboardVendor = GetOnboardVendor.as_view("GetOnboardVendor")
GetPo = GetPo.as_view("GetPo")
GetPoForm = GetPoForm.as_view("GetPoForm")
user_verification = user_verification.as_view("user_verification")
CRForminitSubmitted = CRForminitSubmitted.as_view("CRForminitSubmitted")
user_heading = user_heading.as_view("user_heading")
CRForminitAccess = CRForminitAccess.as_view("CRForminitAccess")
find_attachment_from_unique_id = find_attachment_from_unique_id.as_view("find_attachment_from_unique_id")
find_attachment_with_page = find_attachment_with_page.as_view("find_attachment_with_page")



# # # adding routes to the Views we just created
CRForm_view.add_url_rule('/cr_form_group', view_func=CreateCRFormGroup, methods=['POST'])
CRForm_view.add_url_rule('/update_cr_form_group_status', view_func=UpdateCrFormGroupStatus, methods=['POST'])
CRForm_view.add_url_rule('/update_cr_form_group', view_func=UpdateCrFormGroup, methods=['POST'])
CRForm_view.add_url_rule('/get_cr_from_group/<page_no>', view_func=GetCrFormGroup, methods=['GET'])
CRForm_view.add_url_rule('/cr_form', view_func=CreateCRForm, methods=['POST'])
CRForm_view.add_url_rule('/cr_form_initiate', view_func=CreateCRForminit, methods=['POST'])
CRForm_view.add_url_rule('/view_cr_form', view_func=ViewCRForm, methods=['POST'])
CRForm_view.add_url_rule('/update_cr_form_status', view_func=UpdateCrFormStatus, methods=["POST"])
CRForm_view.add_url_rule('/get_cr_form_by_slug/<slug>', view_func=GetCrFormBySlug, methods=["GET"])
CRForm_view.add_url_rule('/get_cr_form/<page_no>', view_func=GetCrForm, methods=["GET"])
CRForm_view.add_url_rule('/add_po_master', view_func=CreatePOMaster, methods=["POST"])
CRForm_view.add_url_rule('/update_po_master_status', view_func=UpdatePOMasterStatus, methods=["POST"])
CRForm_view.add_url_rule('/update_po_master', view_func=UpdatePOMaster, methods=['POST'])
CRForm_view.add_url_rule('/get_po_master', view_func=GetPoMaster, methods=['POST'])  # change
CRForm_view.add_url_rule('/add_vendors', view_func=CreateVendors, methods=['POST'])
CRForm_view.add_url_rule('/update_vendor_status', view_func=UpdateVendorStatus, methods=['POST'])
CRForm_view.add_url_rule('/update_vendor', view_func=UpdateVendor, methods=['POST'])
CRForm_view.add_url_rule('/get_vendors', view_func=GetVendor, methods=['POST'])
CRForm_view.add_url_rule("/cr_form_user_initialize", view_func=CRForminit, methods=['POST'])
CRForm_view.add_url_rule("/release_user_cr_form", view_func=RECRForminit, methods=['POST'])
CRForm_view.add_url_rule("/form_initialize", view_func=Forminit, methods=['POST'])
CRForm_view.add_url_rule('/get_dvalue_by_dcode', view_func=GetDemogValueById, methods=['POST'])
CRForm_view.add_url_rule('/get_onboard_vendor', view_func=GetOnboardVendor, methods=['POST'])
CRForm_view.add_url_rule('/get_po', view_func=GetPo, methods=['POST'])
CRForm_view.add_url_rule('/get_po_form', view_func=GetPoForm, methods=['POST'])
CRForm_view.add_url_rule('/user_verify_by_costctnr', view_func=user_verification, methods=['POST'])
CRForm_view.add_url_rule('/cr_form_submitted', view_func=CRForminitSubmitted, methods=['POST'])
CRForm_view.add_url_rule('/user_heading', view_func=user_heading, methods=['POST'])
CRForm_view.add_url_rule('/cr_form_initial_access', view_func=CRForminitAccess, methods=['POST'])
CRForm_view.add_url_rule('/find_attachment_from_unique_id', view_func=find_attachment_from_unique_id, methods=['POST'])
CRForm_view.add_url_rule('/find_attachment_with_page', view_func=find_attachment_with_page, methods=['POST'])

