import json
from app import db
from app import ma
from flask import Blueprint, Flask, jsonify, make_response, request
from sqlalchemy.orm.attributes import QueryableAttribute
import datetime
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema

current_timestamp = datetime.datetime.now()


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), nullable=False)
    costcntr = db.Column(db.String(20), nullable=True)
    employment_type = db.Column(db.String(20), nullable=True)
    alpeta_user_id = db.Column(db.Integer, nullable=True)
    designation_id = db.Column(db.Integer, nullable=True)
    role_id = db.Column(db.Integer, nullable=True)
    shift_id = db.Column(db.Integer, nullable=True)
    full_name = db.Column(db.String(128), nullable=True)
    dob = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    nationality = db.Column(db.String(10),nullable=True)
    marital_status = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    phone = db.Column(db.String(50),nullable=True)
    esi_no = db.Column(db.String(50), nullable=True )
    pf_no = db.Column(db.String(50), nullable=True)
    employment_start_date = db.Column(db.DateTime, nullable=True)
    employment_end_date = db.Column(db.DateTime, nullable=True)
    employment_separation_date = db.Column(db.DateTime, nullable=True)
    password = db.Column(db.String(128), nullable=False)
    alpeta_password = db.Column(db.Integer, nullable=False)
    # profile_picture = db.Column(db.String(255))
    status = db.Column(db.String(10), nullable=False)
    last_updated_by = db.Column(db.String(20), nullable=True)
    last_update_date = db.Column(db.DateTime, nullable=True)
    is_deleted = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    alpeta_created_date = db.Column(db.DateTime, nullable=True)
    alpeta_updated_date = db.Column(db.DateTime, nullable=True)
    auth_comb = db.Column(db.String(255), nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    group_assign_date = db.Column(db.DateTime, nullable=True)
    group_updated_date = db.Column(db.DateTime, nullable=True)
    separation_reason = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(50), nullable=True)
    cl_scrum_id = db.Column(db.String(50), nullable=True)
    vd_scrum_id = db.Column(db.String(50), nullable=True)
    scrum_wo_id = db.Column(db.String(50), nullable=True)
    aadhaar = db.Column(db.String(50), nullable=True)
    registration_done = db.Column(db.String(50), nullable=True)
    vendor_id = db.Column(db.String(50), nullable=True)

    def __init__(self, employee_id, costcntr, employment_type, alpeta_user_id, designation_id, role_id,
                 shift_id,
                 full_name, dob, gender, nationality, marital_status, address, email, phone, esi_no, pf_no
                 , employment_start_date, employment_end_date, employment_separation_date, password, alpeta_password,
                 # profile_picture,
                 status, last_updated_by, last_update_date, is_deleted, created_at, updated_at,
                 alpeta_created_date, alpeta_updated_date, auth_comb, group_id, group_assign_date, group_updated_date,
                 separation_reason, unit, cl_scrum_id, vd_scrum_id, scrum_wo_id, aadhaar, registration_done, vendor_id):
        self.employee_id = employee_id
        self.costcntr = costcntr
        self.employment_type = employment_type
        self.alpeta_user_id = alpeta_user_id
        self.designation_id = designation_id
        self.role_id = role_id
        self.shift_id = shift_id
        self.full_name = full_name
        self.dob = dob
        self.gender = gender
        self.nationality = nationality
        self.marital_status = marital_status
        self.address = address
        self.email = email
        self.phone = phone
        self.esi_no = esi_no
        self.pf_no = pf_no
        self.employment_start_date = employment_start_date
        self.employment_end_date = employment_end_date
        self.employment_separation_date = employment_separation_date
        self.password = password
        self.alpeta_password = alpeta_password
        # self.profile_picture = profile_picture
        self.status = status
        self.last_updated_by = last_updated_by
        self.last_update_date = last_update_date
        self.is_deleted = is_deleted
        self.created_at = created_at
        self.updated_at = updated_at
        self.alpeta_created_date = alpeta_created_date
        self.alpeta_updated_date = alpeta_updated_date
        self.auth_comb = auth_comb
        self.group_id = group_id
        self.group_assign_date = group_assign_date
        self.group_updated_date = group_updated_date
        self.separation_reason = separation_reason
        self.unit = unit
        self.cl_scrum_id = cl_scrum_id
        self.vd_scrum_id = vd_scrum_id
        self.scrum_wo_id = scrum_wo_id
        self.aadhaar = aadhaar
        self.registration_done = registration_done
        self.vendor_id = vendor_id

    def addUser(employee_id, costcntr, alpeta_user_id, employment_type, designation_id,
                role_id, shift_id, full_name, dob, gender, nationality, marital_status,
                address, email, phone, esi_no, pf_no, password, alpeta_password, auth_comb):
        addedUser = Users(employee_id=employee_id,
                          costcntr=costcntr,
                          employment_type=employment_type,
                          alpeta_user_id=int(alpeta_user_id),
                          designation_id=int(designation_id),
                          role_id=int(role_id),
                          shift_id=int(shift_id),
                          full_name=full_name,
                          dob=dob,
                          gender=gender,
                          nationality=nationality,
                          marital_status=marital_status,
                          address=address,
                          email=email,
                          phone=phone,
                          esi_no=esi_no,
                          pf_no=pf_no,
                          employment_start_date=None,
                          employment_end_date=None,
                          employment_separation_date=None,
                          password=password,
                          alpeta_password=int(alpeta_password),
                          # profile_picture=profile_picture,
                          status='active',
                          last_updated_by=None,
                          last_update_date=None,
                          is_deleted=0,
                          created_at=current_timestamp,
                          updated_at=current_timestamp,
                          alpeta_created_date=current_timestamp,
                          alpeta_updated_date=current_timestamp,
                          auth_comb=auth_comb,
                          group_id=None
                          )
        db.session.add(addedUser)
        db.session.commit()
        return addedUser

    def UpadteUser(id, employee_id, costcntr, vendor_id, employment_type, alpeta_user_id, designation_id, role_id,
                   shift_id, full_name, dob, gender, nationality, marital_status, address, email, phone, esi_no, pf_no
                   , employment_start_date, employment_end_date, employment_separation_date, password, alpeta_password):
        # profile_picture):
        Users.query.filter(Users.id == id).update({Users.employee_id: employee_id,
                                                   Users.costcntr: costcntr,
                                                   Users.vendor_id: vendor_id,
                                                   Users.employment_type: employment_type,
                                                   Users.alpeta_user_id: alpeta_user_id,
                                                   Users.designation_id: designation_id,
                                                   Users.role_id: role_id,
                                                   Users.shift_id: shift_id,
                                                   Users.full_name: full_name,
                                                   Users.dob: dob,
                                                   Users.gender: gender,
                                                   Users.nationality: nationality,
                                                   Users.marital_status: marital_status,
                                                   Users.address: address,
                                                   Users.email: email,
                                                   Users.phone: phone,
                                                   Users.esi_no: esi_no,
                                                   Users.pf_no: pf_no,
                                                   Users.employment_start_date: employment_start_date,
                                                   Users.employment_end_date: employment_end_date,
                                                   Users.employment_separation_date: employment_separation_date,
                                                   Users.password: password,
                                                   Users.alpeta_password: alpeta_password,
                                                   # Users.profile_picture: profile_picture,
                                                   Users.alpeta_updated_date: current_timestamp,
                                                   Users.alpeta_created_date: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Fetch_user(_email):
        query = Users.query.filter_by(email=_email).first()
        return query

    def FetchUSerDetails_By_ID(_id):
        query = Users.query.filter_by(id=_id).first()
        UserSchema = User_schema()
        # UserSchema = User_schema(many=True)
        output = UserSchema.dump(query)
        return output

    def FetchUSerDetails_By_alpeta_ID(alpeta_id):
        alpeta_id = int(alpeta_id)
        query = Users.query.filter_by(alpeta_user_id=alpeta_id).with_entities(Users.group_id).first()
        UserSchema = User_schema()
        output = UserSchema.dump(query)
        return output.get("group_id")

    def FetchUSerDetails_By_group_id(group_id):
        query = Users.query.filter_by(group_id=group_id).all()
        # UserSchema = User_schema()
        UserSchema = User_schema(many=True)
        output = UserSchema.dump(query)
        return output
    
    def FetchUSerDetails_By_clms_id(_employee_id):
        query = Users.query.filter_by(employee_id=_employee_id).first()
        UserSchema = User_schema()
        output = UserSchema.dump(query)
        if output:
            output["unique_id"] = cr_dd.get_demog_value_by_demog_value(output["aadhaar"])["unique_id"]
        else:
            output["unique_id"] = None
        return output
        
    def FetchUSerDetails_By_vendor_id(_vendor_id):
        query = Users.query.filter_by(vendor_id=_vendor_id, status="active").all()
        # UserSchema = User_schema()
        UserSchema = User_schema(many=True)
        output = UserSchema.dump(query)
        return len(output)
        # UserSchema = User_schema()
        UserSchema = User_schema(many=True)
        output = UserSchema.dump(query)
        return len(output)
    
    def FetchUSerDetails_By_employee_id(_employee_id):
        query = Users.query.filter_by(employee_id=_employee_id). \
            with_entities(Users.full_name, Users.employee_id, Users.designation_id, Users.costcntr).first()
        UserSchema = User_schema()
        output = UserSchema.dump(query)
        return output

    def Delete(_id):
        Users.query.filter_by(id=_id).delete()
        db.session.commit()

        def __repr__(self):
            userObject = {
                "id": self.id,
                "employee_id": self.employee_id,
                "costcntr": self.costcntr,
                "full_name": self.full_name,
            }

            return json.dumps(userObject)


class User_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subarea_id = db.Column(db.Integer)
    costcntr = db.Column(db.String(28))
    shop_name = db.Column(db.String(28))
    dept_group = db.Column(db.String(20))
    hod_man = db.Column(db.String(20))
    hod_functional_area = db.Column(db.String(20))
    clms_nodal_user = db.Column(db.String(20))
    clms_nodal_ajs = db.Column(db.String(20))
    clms_nodal_secu = db.Column(db.String(20))
    clms_nodal_hr = db.Column(db.String(20))
    clms_nodal_safety = db.Column(db.String(20))
    clms_nodal_medical = db.Column(db.String(20))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, subarea_id, costcntr, shop_name, dept_group, hod_man, hod_functional_area,
                 clms_nodal_user, clms_nodal_ajs, clms_nodal_secu, clms_nodal_hr, clms_nodal_safety, clms_nodal_medical,
                 status, created_at, updated_at):
        self.subarea_id = subarea_id
        self.costcntr = costcntr
        self.shop_name = shop_name
        self.dept_group = dept_group
        self.hod_man = hod_man
        self.hod_functional_area = hod_functional_area
        self.clms_nodal_user = clms_nodal_user
        self.clms_nodal_ajs = clms_nodal_ajs
        self.clms_nodal_secu = clms_nodal_secu
        self.clms_nodal_hr = clms_nodal_hr
        self.clms_nodal_safety = clms_nodal_safety
        self.clms_nodal_medical = clms_nodal_medical
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def FetchDEpartmentDetails_By_ID(id):
        query = Department.query.filter_by(id=id).first()
        DeptSchema = Department_schema()
        # DeptSchema = Department_schema(many=True)
        output = DeptSchema.dump(query)
        return output

    def FetchDEpartmentDetails_By_Cost_center(costcntr):
        query = Department.query.filter_by(costcntr=costcntr).first()
        DeptSchema = Department_schema()
        output = DeptSchema.dump(query)
        return output
        
    def check_ROW_if_exists_in_Table(employee_id):
        query = Department.query.filter(
            (Department.clms_nodal_user == employee_id) | (Department.hod_man == employee_id) | (
                        Department.hod_functional_area == employee_id)).all()
        DeptSchema = Department_schema(many=True)
        output = DeptSchema.dump(query)
        if len(output) is 0:
            return False
        else:
            return True
            

    def Add_Department(subarea_id, costcntr, shop_name, dept_group, hod_man, hod_functional_area,
                       clms_nodal_user, clms_nodal_ajs, clms_nodal_secu, clms_nodal_hr, clms_nodal_safety,
                       clms_nodal_medical,
                       status):
        Query = Department(subarea_id=int(subarea_id),
                           costcntr=costcntr,
                           shop_name=shop_name,
                           dept_group=dept_group,
                           hod_man=hod_man,
                           hod_functional_area=hod_functional_area,
                           clms_nodal_user=clms_nodal_user,
                           clms_nodal_ajs=clms_nodal_ajs,
                           clms_nodal_secu=clms_nodal_secu,
                           clms_nodal_hr=clms_nodal_hr,
                           clms_nodal_safety=clms_nodal_safety,
                           clms_nodal_medical=clms_nodal_medical,
                           status=status,
                           created_at=current_timestamp,
                           updated_at=current_timestamp)
        db.session.add(Query)
        db.session.commit()

    def DepartmentsBySUBareaID(subarea_id):
        query = Department.query.filter(Department.subarea_id == subarea_id, Department.status != 'delete').all()
        return query

    def Update_Department(id, subarea_id, costcntr, shop_name, dept_group, hod_man, hod_functional_area,
                          clms_nodal_user, clms_nodal_ajs, clms_nodal_secu, clms_nodal_hr, clms_nodal_safety,
                          clms_nodal_medical):
        Department.query.filter(Department.id == id).update({Department.subarea_id: subarea_id,
                                                             Department.costcntr: costcntr,
                                                             Department.shop_name: shop_name,
                                                             Department.dept_group: dept_group,
                                                             Department.hod_man: hod_man,
                                                             Department.hod_functional_area: hod_functional_area,
                                                             Department.clms_nodal_user: clms_nodal_user,
                                                             Department.clms_nodal_ajs: clms_nodal_ajs,
                                                             Department.clms_nodal_secu: clms_nodal_secu,
                                                             Department.clms_nodal_hr: clms_nodal_hr,
                                                             Department.clms_nodal_safety: clms_nodal_safety,
                                                             Department.clms_nodal_medical: clms_nodal_medical,
                                                             Department.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Change_Status(_id, _status):
        Department.query.filter(Department.id == _id).update({Department.status: _status,
                                                              Department.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()
    
    def get_department_by_costcenter(costcenter):
        query = Department.query.filter(Department.costcntr == str(costcenter)). \
            with_entities(Department.clms_nodal_user, Department.clms_nodal_ajs, Department.clms_nodal_hr,
                          Department.clms_nodal_secu, Department.hod_man, Department.hod_functional_area).first()
        DeptSchema = Department_schema()
        output = DeptSchema.dump(query)
        return output

    def Delete(_id):
        Department.query.filter_by(id=_id).delete()
        db.session.commit()


class Department_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Department


class Shifts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(20))
    shift_start_time = db.Column(db.DateTime)
    shift_end_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, name, code, shift_start_time, shift_end_time, status, created_at, updated_at):
        self.name = name
        self.code = code
        self.shift_start_time = shift_start_time
        self.shift_end_time = shift_end_time
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def FetchShiftsDetails_By_ID(id):
        query = Shifts.query.filter_by(id=id).first()
        ShiftSchema = Shifts_schema()
        # ShiftSchema = Shifts_schema(many=True)
        output = ShiftSchema.dump(query)
        return output

    def Add_shifts(_name, _code, _shift_start_time, _shift_end_time, _status):
        Query = Shifts(name=_name, code=_code, shift_start_time=_shift_start_time,
                       shift_end_time=_shift_end_time, status=_status, created_at=current_timestamp,
                       updated_at=current_timestamp)
        db.session.add(Query)
        db.session.commit()

    def Update_Shifts(_id, _name, _code, _shift_start_time, _shift_end_time):
        Shifts.query.filter(Shifts.id == _id).update({Shifts.name: _name,
                                                      Shifts.code: _code,
                                                      Shifts.shift_start_time: _shift_start_time,
                                                      Shifts.shift_end_time: _shift_end_time,
                                                      Shifts.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

        # user = User.query.filter_by(id=_id).first()
        # response = {"first_name": user.first_name, "last_name": user.last_name}

    def Change_Status(_id, _status):
        Shifts.query.filter(Shifts.id == _id).update({Shifts.status: _status, Shifts.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Delete(_id):
        Shifts.query.filter_by(id=_id).delete()
        db.session.commit()


class Shifts_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Shifts


class Designations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    name = db.Column(db.String(50))
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, code, name, status, created_at, updated_at):
        self.code = code
        self.name = name
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def FetchDesignationDetails_By_ID(id):
        query = Designations.query.filter_by(id=id).first()
        DesignationSchema = Designations_schema()
        output = DesignationSchema.dump(query)
        return output

    def Add_Designations(_name, _code, _status):
        Query = Designations(name=_name,
                             code=_code,
                             status=_status,
                             created_at=current_timestamp,
                             updated_at=current_timestamp)
        db.session.add(Query)
        db.session.commit()

    def Update_Designation(_id, _name, _code):
        Designations.query.filter(Designations.id == _id).update({Designations.name: _name,
                                                                  Designations.code: _code,
                                                                  Designations.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

        # user = User.query.filter_by(id=_id).first()
        # response = {"first_name": user.first_name, "last_name": user.last_name}

    def Change_Status(_id, _status):
        Designations.query.filter(Designations.id == _id).update(
            {Designations.status: _status, Designations.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Delete(_id):
        Designations.query.filter_by(id=_id).delete()
        db.session.commit()


class Designations_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Designations


class User_cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    cardnum = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, user_id, cardnum, created_at, updated_at):
        self.user_id = user_id
        self.cardnum = cardnum
        self.created_at = created_at
        self.updated_at = updated_at

    def FetchUserCardsDetails_By_ID(user_id):
        query = User_cards.query.filter_by(user_id=user_id).first()
        UsercardsSchema = User_cards_schema()
        output = UsercardsSchema.dump(query)
        return output

    def addCards(user_id, cardnum):
        add = User_cards(user_id=user_id, cardnum=cardnum, created_at=current_timestamp, updated_at=current_timestamp)
        db.session.add(add)
        db.session.commit()

    def Delete(_id):
        User_cards.query.filter_by(user_id=_id).delete()
        db.session.commit()


class User_cards_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = User_cards


class User_terminals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    terminal_id = db.Column(db.Integer)
    is_block = db.Column(db.Integer)
    block_from = db.Column(db.DateTime)
    block_to = db.Column(db.DateTime)
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, user_id, terminal_id, is_block, block_from, block_to, status, created_at, updated_at):
        self.user_id = user_id
        self.terminal_id = terminal_id
        self.is_block = is_block
        self.block_from = block_from
        self.block_to = block_to
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def Get_Terminals_by_userID(UserID):
        query = User_terminals.query.with_entities(User_terminals.terminal_id).filter(
            User_terminals.user_id == UserID).all()
        Groupterminalsschema = User_terminals_schema(many=True)
        output = Groupterminalsschema.dump(query)
        return [i["terminal_id"] for i in output]

    def Get_Terminals_by_userID_status(UserID):
        # query = User_terminals.query.with_entities(User_terminals.terminal_id, User_terminals.is_block).filter(
        #     User_terminals.user_id == UserID).all()
        query = User_terminals.query.filter(
            User_terminals.user_id == UserID).all()
        Groupterminalsschema = User_terminals_schema(many=True)
        output = Groupterminalsschema.dump(query)
        return output

    def Get_Terminals_by_userID_blacklist_status_(UserID):
        # query = User_terminals.query.with_entities(User_terminals.terminal_id, User_terminals.is_block).filter(
        #     User_terminals.user_id == UserID).all()
        query = User_terminals.query.filter(
            User_terminals.user_id == UserID, User_terminals.is_block != 1).all()
        Groupterminalsschema = User_terminals_schema(many=True)
        output = Groupterminalsschema.dump(query)
        return [i["terminal_id"] for i in output]

    def Get_USers_by_TerminalID(TerminalID):
        query = User_terminals.query.with_entities(User_terminals.user_id).filter(
            User_terminals.terminal_id == TerminalID).all()
        Groupterminalsschema = User_terminals_schema(many=True)
        output = Groupterminalsschema.dump(query)
        return [i["user_id"] for i in output]

    def Add_User_Terminals(user_id, terminal_id, status):
        Query = User_terminals(user_id=user_id,
                               terminal_id=terminal_id,
                               is_block=0,
                               block_from=None,
                               block_to=None,
                               status=status,
                               created_at=current_timestamp,
                               updated_at=current_timestamp)
        db.session.add(Query)
        db.session.commit()

    def Update_User_terminals(id, user_id, terminal_id, is_block, block_from, block_to, updated_at):
        User_terminals.query.filter(User_terminals.id == id).update({User_terminals.user_id: user_id,
                                                                     User_terminals.terminal_id: terminal_id,
                                                                     User_terminals.is_block: is_block,
                                                                     User_terminals.block_from: block_from,
                                                                     User_terminals.block_to: block_to,
                                                                     User_terminals.updated_at: updated_at})
        db.session.flush()
        db.session.commit()

    def Change_Status(_id, _status):
        User_terminals.query.filter(User_terminals.id == _id).update(
            {User_terminals.status: _status, User_terminals.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def check_ROW_if_exists_in_Table(terminal_id, user_id):
        query = User_terminals.query.filter(User_terminals.terminal_id == terminal_id,
                                            User_terminals.user_id == user_id).first()
        Groupterminalsschema = Group_terminals_schema()
        output = Groupterminalsschema.dump(query)
        if len(output) is 0:
            return False
        else:
            return True
    
    def get_id_by_terminal_user(terminal_id, user_id):
        query = User_terminals.query.filter(User_terminals.terminal_id == terminal_id,
                                            User_terminals.user_id == user_id).\
            with_entities(User_terminals.id).first()
        Groupterminalsschema = Group_terminals_schema()
        output = Groupterminalsschema.dump(query)
        return output.get("id",None)

    def Delete(_id, user_id):
        User_terminals.query.filter_by(terminal_id=_id, user_id=user_id).delete()
        # print(User_terminals.query.filter(User_terminals.id == _id, User_terminals.user_id == user_id))
        db.session.commit()

    def GET_id_to_be_deleted(terminal_id, user_id):
        query = User_terminals.query.filter(User_terminals.terminal_id == terminal_id,
                                            User_terminals.user_id == user_id).first()
        Groupterminalsschema = Group_terminals_schema()
        output = Groupterminalsschema.dump(query)
        if len(output) > 0:
            return output["id"]
        else:
            return None

    def Delete_by_row_id(id):
        User_terminals.query.filter_by(id=id).delete()
        db.session.commit()


class User_terminals_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = User_terminals


class Terminals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    alpeta_terminal_id = db.Column(db.Integer)
    short_code = db.Column(db.String(10))
    terminal_type = db.Column(db.String(10))
    description = db.Column(db.String(128))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, name, alpeta_terminal_id, short_code, terminal_type, description, status, created_at,
                 updated_at):
        self.name = name
        self.alpeta_terminal_id = alpeta_terminal_id
        self.short_code = short_code
        self.terminal_type = terminal_type
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def FetchTerminals_By_ID(id):
        query = Terminals.query.filter_by(id=id).first()
        termnlSchema = Terminals_schema()
        output = termnlSchema.dump(query)
        return output

    def FetchTerminals_By_AlpetaID(Alpeta_ID):
        query = Terminals.query.filter_by(alpeta_terminal_id=Alpeta_ID).first()
        termnlSchema = Terminals_schema()
        output = termnlSchema.dump(query)
        return output

    def Add_terminals(name, alpeta_terminal_id, short_code, terminal_type, description, status):
        Query = Terminals(name=name,
                          alpeta_terminal_id=alpeta_terminal_id,
                          short_code=short_code,
                          terminal_type=terminal_type,
                          description=description,
                          status=status,
                          created_at=current_timestamp,
                          updated_at=current_timestamp)
        db.session.add(Query)
        db.session.commit()

    def Update_Terminals(_id, name, alpeta_terminal_id, short_code, terminal_type, description, ):
        Terminals.query.filter(Terminals.id == _id).update({Terminals.name: name,
                                                            Terminals.alpeta_terminal_id: alpeta_terminal_id,
                                                            Terminals.short_code: short_code,
                                                            Terminals.terminal_type: terminal_type,
                                                            Terminals.description: description,
                                                            Terminals.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Change_Status(_id, _status):
        Terminals.query.filter(Terminals.id == _id).update(
            {Terminals.status: _status, Terminals.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Delete(_id):
        Terminals.query.filter_by(id=_id).delete()
        db.session.commit()


class Terminals_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Terminals


class User_fingerprints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    alpeta_user_id = db.Column(db.Integer)
    fingerid = db.Column(db.Integer)
    totalsize = db.Column(db.Integer)
    template1 = db.Column(db.String)
    template2 = db.Column(db.String)
    convimage1 = db.Column(db.String)
    convimage2 = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, user_id, alpeta_user_id, fingerid, totalsize, template1, template2,
                 convimage1, convimage2, created_at, updated_at):
        self.user_id = user_id
        self.alpeta_user_id = alpeta_user_id
        self.fingerid = fingerid
        self.totalsize = totalsize
        self.template1 = template1
        self.template2 = template2
        self.convimage1 = convimage1
        self.convimage2 = convimage2
        self.created_at = created_at
        self.updated_at = updated_at

    def FetchUserFingerPrintDetails_By_ID(user_id):
        query = User_fingerprints.query.filter_by(user_id=user_id).all()
        UserFprintsSchema = User_fingerprints_schema()
        UserFprintsSchema = User_fingerprints_schema(many=True)
        output = UserFprintsSchema.dump(query)
        return output

    def add_fingerprint(user_id, alpeta_user_id, fingerid, totalsize, template1, template2, convimage1, convimage2):
        addFingerPrint = User_fingerprints(user_id=user_id, alpeta_user_id=alpeta_user_id, fingerid=fingerid,
                                           totalsize=totalsize, template1=template1, template2=template2,
                                           convimage1=convimage1, convimage2=convimage2, created_at=current_timestamp,
                                           updated_at=current_timestamp)

        db.session.add(addFingerPrint)
        db.session.commit()
        id = addFingerPrint.id
        return id

    def Delete(_id):
        User_fingerprints.query.filter_by(user_id=_id).delete()
        db.session.commit()


class User_fingerprints_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = User_fingerprints


class Subarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    name = db.Column(db.String(50))
    description = db.Column(db.String(128))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, code, name, description, status, created_at, updated_at):
        self.code = code
        self.name = name
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def FetchSubareaDetails_By_ID(user_id):
        query = Subarea.query.filter_by(user_id=user_id).first()
        subarea = Subarea_schema()
        output = subarea.dump(query)
        return output

    def Add_Subarea(_code, _name, _description, _status):
        Query = Subarea(code=_code, name=_name,
                        description=_description, status=_status,
                        created_at=current_timestamp, updated_at=current_timestamp)

        db.session.add(Query)
        db.session.commit()

    def Update_Subarea(_id, _code, _name, _description):
        Subarea.query.filter(Subarea.id == _id).update({Subarea.code: _code,
                                                        Subarea.name: _name,
                                                        Subarea.description: _description,
                                                        Subarea.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

        # user = User.query.filter_by(id=_id).first()
        # response = {"first_name": user.first_name, "last_name": user.last_name}

    def Change_Status(_id, _status):
        Subarea.query.filter(Subarea.id == _id).update({Subarea.status: _status, Subarea.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Delete(_id):
        Subarea.query.filter_by(id=_id).delete()
        db.session.commit()


class Subarea_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Subarea


class User_facedatas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    templatesize = db.Column(db.Integer)
    templatedata = db.Column(db.String)
    templatetype = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, user_id, templatesize, templatedata, templatetype, created_at, updated_at):
        self.user_id = user_id
        self.templatesize = templatesize
        self.templatedata = templatedata
        self.templatetype = templatetype
        self.created_at = created_at
        self.updated_at = updated_at

    def FetchUserfacedatas_By_ID(user_id):
        query = User_facedatas.query.filter_by(user_id=user_id).first()
        UserFacedatasSchema = User_facedatas_schema()
        output = UserFacedatasSchema.dump(query)
        return output

    def AddFaceData(user_id, templatesize, templatedata, templatetype):
        Add = User_facedatas(user_id=user_id,
                             templatesize=templatesize,
                             templatedata=templatedata,
                             templatetype=templatetype,
                             created_at=current_timestamp,
                             updated_at=current_timestamp)
        db.session.add(Add)
        db.session.commit()

    def Delete(_id):
        User_facedatas.query.filter_by(id=_id).delete()
        db.session.commit()


class User_facedatas_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = User_facedatas


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    punch_type = db.Column(db.String(10))
    punch_time = db.Column(db.DateTime)
    terminal_id = db.Column(db.Integer)
    sap_sync = db.Column(db.Boolean)
    sap_sync_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, user_id, punch_type, punch_time, terminal_id, sap_sync, sap_sync_time, created_at, updated_at):
        self.user_id = user_id
        self.punch_type = punch_type
        self.punch_time = punch_time
        self.terminal_id = terminal_id
        self.sap_sync = sap_sync
        self.sap_sync_time = sap_sync_time
        self.created_at = created_at
        self.updated_at = updated_at


class Attendance_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance


class role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    slug = db.Column(db.String(20))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, name, slug, status, created_at, updated_at):
        self.name = name
        self.slug = slug
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at


class role_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = role


class Finger_masters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alpeta_value = db.Column(db.Integer)
    name = db.Column(db.String(20))

    def __init__(self, alpeta_value, name):
        self.alpeta_value = alpeta_value
        self.name = name


class Finger_masters_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Finger_masters


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(128))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, name, description, status, created_at, updated_at):
        self.name = name
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def FetchGroupDetails_By_ID(id):
        query = Group.query.filter_by(id=id).first()
        GroupSchema = Group_schema()
        output = GroupSchema.dump(query)
        return output

    def Add_Group(_name, _description, _status):
        Query = Group(name=_name,
                      description=_description,
                      status=_status,
                      created_at=current_timestamp,
                      updated_at=current_timestamp)
        db.session.add(Query)
        db.session.commit()

    def Update_Group(_id, _name, _description):
        Group.query.filter(Group.id == _id).update({Group.name: _name,
                                                    Group.description: _description,
                                                    Group.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Change_Status(_id, _status):
        Group.query.filter(Group.id == _id).update({Group.status: _status,
                                                    Group.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Delete(_id):
        Group.query.filter_by(id=_id).delete()
        db.session.commit()


class Group_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Group


class Group_terminals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    terminal_id = db.Column(db.Integer)
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, group_id, terminal_id, status, created_at, updated_at):
        self.group_id = group_id
        self.terminal_id = terminal_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def check_terminal_if_exists_in_group(terminal_id, group_id):
        query = Group_terminals.query.filter(Group_terminals.terminal_id == terminal_id,
                                             Group_terminals.group_id == group_id).all()
        Groupterminalsschema = Group_terminals_schema(many=True)
        output = Groupterminalsschema.dump(query)
        if len(output) is 0:
            return True
        else:
            return False

    def GET_TerminalsDEtails_BY_GRoupID(GroupID):
        query = Group_terminals.query.with_entities(Group_terminals.terminal_id).filter(
            Group_terminals.group_id == GroupID).all()
        Groupterminalsschema = Group_terminals_schema(many=True)
        output = Groupterminalsschema.dump(query)
        # return output
        return [i["terminal_id"] for i in output]

    def GET_GroupID_BY_terminalID(TermianlID):
        query = Group_terminals.query.with_entities(Group_terminals.group_id).filter(
            Group_terminals.terminal_id == TermianlID).all()
        Groupterminalsschema = Group_terminals_schema(many=True)
        output = Groupterminalsschema.dump(query)
        return [i["group_id"] for i in output]

    def Add_TerminalToGroup(group_id, terminal_id, status):
        Query = Group_terminals(group_id=group_id,
                                terminal_id=terminal_id,
                                status=status,
                                created_at=current_timestamp,
                                updated_at=current_timestamp)
        db.session.add(Query)
        db.session.commit()

    def Update_TerminalToGroup(group_id, terminal_id):
        Group_terminals.query.filter(Group_terminals.group_id == group_id).update(
            {Group_terminals.terminal_id: terminal_id,
             Group_terminals.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Change_Status(_id, _status):
        Group_terminals.query.filter(Group_terminals.id == _id).update({Group_terminals.status: _status,
                                                                        Group_terminals.updated_at: current_timestamp})
        db.session.flush()
        db.session.commit()

    def Delete(_id, group_id):
        Group_terminals.query.filter(Group_terminals.group_id == group_id,
                                     Group_terminals.terminal_id == _id).delete()

        # Group_terminals.query.filter_by(group_id=_id).delete()
        db.session.commit()

    def DeleteBYgroup_id(group_id):
        # Group_terminals.query.filter(Group_terminals.group_id == group_id).delete()
        Group_terminals.query.filter_by(group_id=group_id).delete()
        db.session.commit()


class Group_terminals_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Group_terminals


class mvw_cl_current_profile(db.Model):
    employee_id = db.Column(db.String(20), primary_key=True)
    full_name = db.Column(db.String(128))
    role_id = db.Column(db.Integer)
    cl_scrum_id = db.Column(db.String(50))
    cl_aadhaar = db.Column(db.String(15))
    cl_gender = db.Column(db.String(10))
    cl_blood_group = db.Column(db.String(10))
    cl_phone = db.Column(db.String(128))
    cl_emergency_no = db.Column(db.String(128))
    cl_guardian_name = db.Column(db.String(128))
    cl_present_address = db.Column(db.String(128))
    cl_permanent_address = db.Column(db.String(128), nullable=True)
    cl_employer = db.Column(db.String(50))
    vd_name = db.Column(db.String(128))
    cl_trade = db.Column(db.String(50))
    cl_pfno = db.Column(db.String(50), nullable=True)
    cl_esino = db.Column(db.String(50))
    cl_uanno = db.Column(db.String(50), nullable=True)
    cl_pcc = db.Column(db.String(50), nullable=True)
    cl_unit = db.Column(db.String(50))
    cl_valid_upto = db.Column(db.String(50), nullable=True)
    cl_active = db.Column(db.String(50), nullable=True)

    def __init__(self, employee_id, full_name, role_id, cl_scrum_id, cl_aadhaar, cl_gender, cl_blood_group,
                 cl_phone, cl_emergency_no, cl_guardian_name, cl_present_address, cl_permanent_address, cl_employer,
                 vd_name, cl_trade, cl_pfno, cl_esino, cl_uanno, cl_pcc, cl_unit, cl_valid_upto, cl_active):
        self.employee_id = employee_id
        self.full_name = full_name
        self.role_id = role_id
        self.cl_scrum_id = cl_scrum_id
        self.cl_aadhaar = cl_aadhaar
        self.cl_gender = cl_gender
        self.cl_blood_group = cl_blood_group
        self.cl_phone = cl_phone
        self.cl_emergency_no = cl_emergency_no
        self.cl_guardian_name = cl_guardian_name
        self.cl_present_address = cl_present_address
        self.cl_permanent_address = cl_permanent_address
        self.cl_employer = cl_employer
        self.vd_name = vd_name
        self.cl_trade = cl_trade
        self.cl_pfno = cl_pfno
        self.cl_esino = cl_esino
        self.cl_uanno = cl_uanno
        self.cl_pcc = cl_pcc
        self.cl_unit = cl_unit
        self.cl_valid_upto = cl_valid_upto
        self.cl_active = cl_active


class mvw_cl_current_profile_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = mvw_cl_current_profile


class mvw_cl_current_detail(db.Model):
    employee_id = db.Column(db.String(20))
    full_name = db.Column(db.String(128))
    dcode = db.Column(db.String(50))
    dvalue = db.Column(db.String(15))
    efrom = db.Column(db.DateTime)
    eto = db.Column(db.DateTime)
    cby = db.Column(db.String(128))
    con = db.Column(db.DateTime)
    did = db.Column(db.String(128), primary_key=True)
    dremarks = db.Column(db.String(128))

    def __init__(self, employee_id, full_name, dcode, dvalue, efrom, eto, cby,
                 con, did, dremarks):
        self.employee_id = employee_id
        self.full_name = full_name
        self.dcode = dcode
        self.dvalue = dvalue
        self.efrom = efrom
        self.eto = eto
        self.cby = cby
        self.con = con
        self.did = did
        self.dremarks = dremarks


class mvw_cl_current_detail_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = mvw_cl_current_detail


class t_attn_raw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pernr = db.Column(db.String(50), nullable=True)
    timr6 = db.Column(db.String(50))
    choic = db.Column(db.String(50))
    ldate = db.Column(db.Date, nullable=True)
    ltime = db.Column(db.String(50), nullable=True)
    satza = db.Column(db.String(50))
    terminal_id = db.Column(db.String(50), nullable=True)
    server_time = db.Column(db.String(50))
    sap_sync_status = db.Column(db.String(50), nullable=True)
    sap_sync_date_time = db.Column(db.DateTime, nullable=True)
    att_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, pernr, timr6, choic, ldate, ltime, satza, terminal_id, server_time, sap_sync_status
                 , att_id, created_at, updated_at):
        self.pernr = pernr
        self.timr6 = timr6
        self.choic = choic
        self.ldate = ldate
        self.ltime = ltime
        self.satza = satza
        self.terminal_id = terminal_id
        self.server_time = server_time
        self.sap_sync_status = sap_sync_status
        self.att_id = att_id
        self.created_at = created_at
        self.updated_at = updated_at

    def Add_attn_raw(_pernr, _timr6, _choic, _ldate, _ltime, _satza, _terminal_id, _server_time, _sap_sync_status
                     , _att_id):
        attendance = t_attn_raw(
            pernr=_pernr,
            timr6=_timr6,
            choic=_choic,
            ldate=_ldate,
            ltime=_ltime,
            satza=_satza,
            terminal_id=_terminal_id,
            server_time=_server_time,
            sap_sync_status=_sap_sync_status,
            att_id=_att_id,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now())
        db.session.add(attendance)
        db.session.commit()


class t_attn_raw_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = t_attn_raw


class user_images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    profile_picture = db.Column(db.String(255))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, user_id, profile_picture, status, created_at, updated_at):
        self.user_id = user_id
        self.profile_picture = profile_picture
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def Add_profile_image(_user_id, _profile_picture, _status):
        user_images.Update_profile_image(_user_id)
        profile_image = user_images(user_id=_user_id,
                                    profile_picture=_profile_picture,
                                    status=_status,
                                    created_at=datetime.datetime.now(),
                                    updated_at=datetime.datetime.now())
        db.session.add(profile_image)
        db.session.commit()

    def FetchProfileImage(_user_id):
        profile_image = user_images.query.filter(user_images.user_id == _user_id,
                                                 user_images.status == "active").first()
        profile_schema = user_images_schema()
        output = profile_schema.dump(profile_image)
        return output

    def Update_profile_image(_user_id):
        user_images.query.filter(user_images.user_id == _user_id, user_images.status == "active").update(
            {
                user_images.status: "inactive",
                user_images.updated_at: datetime.datetime.now()}
        )
        db.session.flush()
        db.session.commit()


class user_images_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = user_images


class dm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    name = db.Column(db.String(50))
    is_required = db.Column(db.Boolean)
    type = db.Column(db.String(24), nullable=True)
    lov_values = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, code, name, is_required, type, lov_values, status, created_at, updated_at):
        self.code = code
        self.name = name
        self.is_required = is_required
        self.type = type
        self.lov_values = lov_values
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def Add_dm(_code, _name, is_required, _type, _value, _status):
        demog_master = dm(code=_code,
                          name=_name,
                          is_required=is_required,
                          type=_type,
                          lov_values=_value,
                          status=_status,
                          created_at=datetime.datetime.now(),
                          updated_at=None
                          )
        db.session.add(demog_master)
        db.session.commit()

    def get_demog_by_id(_id):
        query = dm.query.filter(dm.id == _id).order_by(dm.name).first()
        dmSchema = dm_schema()
        output = dmSchema.dump(query)
        return output

    def get_demog_by_code(_code):
        query = dm.query.filter(dm.code == _code).order_by(dm.updated_at.desc()).first()
        dmSchema = dm_schema()
        output = dmSchema.dump(query)
        return output

    def Change_Status(_id, _status):
        dm.query.filter(dm.id == _id).update(
            {dm.status: _status, dm.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()

    def Update_dm(_id, _code, _name, _is_required, _type, _value):
        dm.query.filter(dm.id == _id).update({dm.code: _code,
                                              dm.name: _name,
                                              dm.is_required: _is_required,
                                              dm.type: _type,
                                              dm.lov_values: _value,
                                              dm.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()

    def Delete_dm(_id):
        dm.query.filter_by(id=_id).delete()
        db.session.commit()


class dm_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = dm


class cr_groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, status, created_at, updated_at):
        self.name = name
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def Add_cr_groups(_name, _status):
        cr_group = cr_groups(
            name=_name,
            status=_status,
            created_at=datetime.datetime.now(),
            updated_at=None
        )
        db.session.add(cr_group)
        db.session.commit()
        
    def get_demog_by_name(name):
        query = cr_groups.query.filter(cr_groups.name == name).order_by(cr_groups.name).first()
        cr_group = cr_groups_schema()
        output = cr_group.dump(query)
        return output

    def Fetch_cr_group_by_groupid(_id):
        query = cr_groups.query.filter(cr_groups.id == _id).order_by(cr_groups.name).first()
        CRGroupSchema = cr_groups_schema()
        output = CRGroupSchema.dump(query)
        print(output)
        return output

    def Change_Status(_id, _status):
        cr_groups.query.filter(cr_groups.id == _id).update(
            {cr_groups.status: _status, cr_groups.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()

    def Update_cr_groups(_id, _name):
        cr_groups.query.filter(cr_groups.id == _id).update({
            cr_groups.name: _name,
            cr_groups.updated_at: datetime.datetime.now()
        })
        db.session.flush()
        db.session.commit()

    def Delete_cr_groups(_id):
        cr_groups.query.filter_by(id=_id).delete()
        db.session.commit()


class cr_groups_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = cr_groups


class cr_demog_groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    demog_id = db.Column(db.String(50))
    group_id = db.Column(db.String(50))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, demog_id, group_id, status, created_at, updated_at):
        self.demog_id = demog_id
        self.group_id = group_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def Add_cr_demog_groups(_demog_id, _group_id, _type, _status):
        cr_demog_group = cr_demog_groups(demog_id=_demog_id,
                                         group_id=_group_id,
                                         status=_status,
                                         created_at=datetime.datetime.now(),
                                         updated_at=None
                                         )
        db.session.add(cr_demog_group)
        db.session.commit()

    def Fetch_cr_demog_group(group_id):
        query = cr_demog_groups.query.with_entities(cr_demog_groups.demog_id). \
            filter(cr_demog_groups.group_id == str(group_id)).order_by(cr_demog_groups.updated_at.desc()).all()
        CrdemongGroupschema = cr_demog_groups_schema(many=True)
        output = CrdemongGroupschema.dump(query)
        return [each.get("demog_id") for each in output]

    def Change_Status(_id, _status):
        cr_demog_groups.query.filter(cr_demog_groups.id == _id).update(
            {cr_demog_groups.status: _status, cr_demog_groups.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()
    
    def Fetch_cr_demog(_demog_id):
        query = cr_demog_groups.query.with_entities(cr_demog_groups.group_id). \
            filter(cr_demog_groups.demog_id == str(_demog_id)).first()
        CrdemongGroupschema = cr_demog_groups_schema()
        output = CrdemongGroupschema.dump(query)
        return output

    def check_terminal_if_exists_in_group(demog_id, group_id):
        query = cr_demog_groups.query.filter(cr_demog_groups.demog_id == str(demog_id),
                                             cr_demog_groups.group_id == str(group_id)).all()
        CrdemongGroupschema = cr_demog_groups_schema(many=True)
        output = CrdemongGroupschema.dump(query)
        if len(output) is 0:
            return True
        else:
            return False

    def Update_cr_demog_groups(_id, _demog_id, _group_id):
        cr_demog_groups.query.filter(cr_demog_groups.id == _id).update({cr_demog_groups.demog_id: _demog_id,
                                                                        cr_demog_groups.group_id: _group_id,
                                                                        cr_demog_groups.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()

    def Delete_cr_demog_groups(_id):
        cr_demog_groups.query.filter_by(id=_id).delete()
        db.session.commit()


class cr_demog_groups_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = cr_demog_groups


class cr_forms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_name = db.Column(db.String(50))
    form_shortcode = db.Column(db.String(50), nullable=True)
    form_description = db.Column(db.String(128), nullable=True)
    form_heading = db.Column(db.String(225), nullable=True)
    form_slug = db.Column(db.String(50))  # need to ask
    form_sub_heading = db.Column(db.String(128), nullable=True)
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, form_name, form_shortcode, form_description, form_heading, form_slug, form_sub_heading,
                 status, created_at, updated_at):
        self.form_name = form_name
        self.form_shortcode = form_shortcode
        self.form_description = form_description
        self.form_heading = form_heading
        self.form_slug = form_slug
        self.form_sub_heading = form_sub_heading
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def Add_cr_form(_form_name, _form_shortcode, _form_description, _form_heading, _form_slug, _form_sub_heading,
                    _status):
        cr_form = cr_forms(form_name=_form_name, form_shortcode=_form_shortcode,
                           form_description=_form_description, form_heading=_form_heading,
                           form_slug=_form_slug, form_sub_heading=_form_sub_heading, status=_status,
                           created_at=datetime.datetime.now(), updated_at=None)
        db.session.add(cr_form)
        db.session.commit()

    def Change_Status(_id, _status):
        cr_forms.query.filter(cr_forms.id == _id).update(
            {cr_forms.status: _status, cr_forms.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()
    
    def Fetch_cr_form(_form_shortcode):
        query = cr_forms.query.filter_by(form_shortcode=_form_shortcode).first()
        CrFormSchema = cr_forms_schema()
        output = CrFormSchema.dump(query)
        return output
        
    def Fetch_cr_form_by_id(_id):
        query = cr_forms.query.filter_by(id=_id).first()
        CrFormSchema = cr_forms_schema()
        output = CrFormSchema.dump(query)
        return output
        
    def Fetch_cr_form_heading_by_id(_id):
        query = cr_forms.query.filter_by(id=_id).with_entities(cr_forms.form_heading,cr_forms.form_slug,cr_forms.form_description,cr_forms.form_sub_heading,cr_forms.form_name).first()
        CrFormSchema = cr_forms_schema()
        output = CrFormSchema.dump(query)
        return output

    def Update_cr_form(_id, _form_name, _form_shortcode, _from_description, _form_heading,
                       _form_slug, _form_sub_heading):
        cr_forms.query.filter(cr_forms.id == _id).update({cr_forms.form_name: _form_name,
                                                          cr_forms.form_shortcode: _form_shortcode,
                                                          cr_forms.form_description: _from_description,
                                                          cr_forms.form_heading: _form_heading,
                                                          cr_forms.form_slug: _form_slug,
                                                          cr_forms.form_sub_heading: _form_sub_heading})


class cr_forms_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = cr_forms


class cr_form_groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.String(50))
    group_id = db.Column(db.String(50))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, form_id, group_id, status, created_at, updated_at):
        self.form_id = form_id
        self.group_id = group_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def Add_cr_form_group(_form_id, _group_id, _status):
        cr_demog_group = cr_form_groups(form_id=_form_id,
                                        group_id=_group_id,
                                        status=_status,
                                        created_at=datetime.datetime.now(),
                                        updated_at=None
                                        )
        db.session.add(cr_demog_group)
        db.session.commit()

    def check_cr_form_if_exists_in_group(_form_id, group_id):
        query = cr_form_groups.query.filter(cr_form_groups.form_id == str(_form_id),
                                            cr_form_groups.group_id == str(group_id)).all()
        CrFormGroupSchema = cr_demog_groups_schema(many=True)
        output = CrFormGroupSchema.dump(query)
        if len(output) is 0:
            return True
        else:
            return False

    def get_cr_form_by_formid(_form_id):
        query = cr_form_groups.query.filter(cr_form_groups.form_id == str(_form_id)). \
            with_entities(cr_form_groups.group_id).all()
        CrFormGroupSchema = cr_demog_groups_schema(many=True)
        output = CrFormGroupSchema.dump(query)
        return [each["group_id"] for each in output]

    def Update_cr_form_groups(_id, _form_id, _group_id):
        cr_form_groups.query.filter(cr_form_groups.id == _id).update({cr_form_groups.form_id: _form_id,
                                                                      cr_form_groups.group_id: _group_id,
                                                                      cr_form_groups.updated_at: datetime.datetime.now()
                                                                      })
        db.session.flush()
        db.session.commit()

    def Change_Status(_id, _status):
        cr_form_groups.query.filter(cr_form_groups.id == _id).update(
            {cr_form_groups.status: _status, cr_form_groups.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()


class cr_form_groups_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = cr_form_groups

class ft_sap_order(db.Model):
    po_number = db.Column(db.String(128), primary_key=True)
    po_date = db.Column(db.String(128), nullable=True)
    po_title = db.Column(db.String(128), nullable=True)
    po_details = db.Column(db.String(255), nullable=True)
    vendor_code = db.Column(db.String(255), nullable=True)
    vendor_name = db.Column(db.String(255), nullable=True)
    vendor_address = db.Column(db.String(255), nullable=True)
    vendor_city = db.Column(db.String(255), nullable=True)
    vendor_active = db.Column(db.String(255), nullable=True)
    gstn = db.Column(db.String(255), nullable=True)

    def __init__(self, po_number, po_date, po_title, po_details, vendor_code, vendor_name, vendor_address, vendor_city,
                 vendor_active, gstn):
        self.po_number = po_number
        self.po_date = po_date
        self.po_title = po_title
        self.po_details = po_details
        self.vendor_code = vendor_code
        self.vendor_name = vendor_name
        self.vendor_address = vendor_address
        self.vendor_city = vendor_city
        self.vendor_active = vendor_active
        self.gstn = gstn


class ft_sap_order_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = ft_sap_order


class po_master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.Integer)
    po_date = db.Column(db.Date)
    po_title = db.Column(db.String(128), nullable=True)
    po_details = db.Column(db.String(255), nullable=True)
    supplier_code = db.Column(db.String(50), nullable=True)
    assign_date = db.Column(db.Date, nullable=True)
    expiry = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, po_number, po_date, po_title, po_details, supplier_code, assign_date, expiry, status, created_at,
                 updated_at):
        self.po_number = po_number
        self.po_date = po_date
        self.po_title = po_title
        self.po_details = po_details
        self.supplier_code = supplier_code
        self.assign_date = assign_date
        self.expiry = expiry
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def Add_po_master(_po_number, _po_date, _po_title, _po_details, _supplier_code, _assign_date, _expiry, _status):
        add_po_master = po_master(po_number=_po_number,
                                  po_date=_po_date,
                                  po_title=_po_title,
                                  po_details=_po_details if _po_details else None,
                                  supplier_code=_supplier_code if _supplier_code else None,
                                  assign_date=_assign_date if _assign_date else None,
                                  expiry=_expiry if _expiry else None,
                                  status=_status,
                                  created_at=datetime.datetime.now(),
                                  updated_at=None
                                  )
        db.session.add(add_po_master)
        db.session.commit()
    
    def check_cr_form_if_exists_in_po(po_number):
        query = po_master.query.filter(po_master.po_number == po_number).first()
        CrFormGroupSchema = po_master_schema()
        output = CrFormGroupSchema.dump(query)
        if len(output) is 0:
            return True
        else:
            return False
    
    def Fetch_po_with_po_number(po_number):
        query = po_master.query.filter(po_master.po_number == po_number).with_entities(po_master.po_date).first()
        CrFormGroupSchema = po_master_schema()
        output = CrFormGroupSchema.dump(query)
        return output
        
    def Fetch_po_expiry_with_po_number(po_number):
        query = po_master.query.filter(po_master.po_number == po_number).with_entities(po_master.expiry).first()
        CrFormGroupSchema = po_master_schema()
        output = CrFormGroupSchema.dump(query)
        return output

    def Change_Status(_id, _status):
        po_master.query.filter(po_master.id == _id).update(
            {po_master.status: _status, po_master.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()

    def Update_po_master(_id, _po_title, _po_details):
        po_master.query.filter(po_master.id == _id).update({
                                                            po_master.po_title: _po_title,
                                                            po_master.po_details: _po_details if _po_details else None,
                                                            po_master.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()


class po_master_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = po_master


class vendors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    vd_code = db.Column(db.String(50))
    vd_scrum_id = db.Column(db.String(50), nullable=True)
    logo = db.Column(db.String(255), nullable=True)
    labour_limit = db.Column(db.Integer)
    unique_id = db.Column(db.String(50), nullable=True)
    is_deleted = db.Column(db.Integer)
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, name, vd_code, vd_scrum_id, logo, labour_limit, unique_id, is_deleted, status, created_at, updated_at):
        self.name = name
        self.vd_code = vd_code
        self.vd_scrum_id = vd_scrum_id
        self.logo = logo
        self.labour_limit = labour_limit
        self.unique_id = unique_id
        self.is_deleted = is_deleted
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def check_cr_form_if_exists_in_vendor(_vd_code):
        query = vendors.query.filter(vendors.vd_code == str(_vd_code)).all()
        VendorSchema = vendors_schema(many=True)
        output = VendorSchema.dump(query)
        if len(output) is 0:
            return True
        else:
            return False

    def Add_vendors(_name, _vd_code, _vd_scrum_id, _logo, _labour_limit, _unique_id, _is_deleted, _status):
        add_vendors = vendors(name=_name, vd_code=_vd_code, vd_scrum_id=_vd_scrum_id, logo=_logo,
                              labour_limit=_labour_limit, unique_id=_unique_id, is_deleted=_is_deleted,
                              status=_status, created_at=datetime.datetime.now(), updated_at=None)
        db.session.add(add_vendors)
        db.session.commit()
        
    def fetch_vendor_by_vendor_code(_vd_code):
        query = vendors.query.filter(vendors.vd_code == str(_vd_code)).first()
        VendorSchema = vendors_schema()
        output = VendorSchema.dump(query)
        return output["labour_limit"]

    def Change_Status(_id, _status):
        vendors.query.filter(vendors.id == _id).update(
            {vendors.status: _status, vendors.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()
        
    def fetch_unique_by_vendor_code(_vd_code):
        query = vendors.query.filter(vendors.vd_code == str(_vd_code)).all()
        VendorSchema = vendors_schema(many=True)
        output = VendorSchema.dump(query)
        return output

    def Update_vendors(_id, _name, _vd_code, _vd_scrum_id, _is_deleted, ):
        vendors.query.filter(vendors.id == _id).update({
            vendors.name: _name,
            vendors.vd_code: _vd_code,
            vendors.vd_scrum_id: _vd_scrum_id,
            vendors.is_deleted: _is_deleted,
            vendors.updated_at: datetime.datetime.now()})
        db.session.flush()
        db.session.commit()


class vendors_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = vendors
        
        

class dd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dcode = db.Column(db.String(50))
    dvalue = db.Column(db.String(15))
    efrom = db.Column(db.DateTime)
    eto = db.Column(db.DateTime)
    cby = db.Column(db.String(128))
    con = db.Column(db.DateTime)
    dremarks = db.Column(db.String(128), nullable=True)
    did = db.Column(db.String(128))
    dkey = db.Column(db.Integer)

    def __init__(self, dcode, dvalue, efrom, eto, cby,
                 con, dremarks, did, dkey):
        self.dcode = dcode
        self.dvalue = dvalue
        self.efrom = efrom
        self.eto = eto
        self.cby = cby
        self.con = con
        self.dremarks = dremarks
        self.did = did
        self.dkey = dkey

    def Add_dd(_dcode, _d_value, _efrom, _eto, _cby, _dremarks, _did, _dkey):
        add_cr_dd = dd(dcode=_dcode, dvalue=_d_value, efrom=datetime.datetime.now(),
                       eto=_eto if _eto else datetime.datetime(9999, 12, 31, 10, 51, 0),
                       cby=_cby, con=datetime.datetime.now(),
                       dremarks=_dremarks, did=_did, dkey=_dkey )
        db.session.add(add_cr_dd)
        db.session.commit()


class cr_dd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dcode = db.Column(db.String(255), nullable=True)
    d_value = db.Column(db.String(255), nullable=True)
    efrom = db.Column(db.Date)
    eto = db.Column(db.Date)
    cby = db.Column(db.String(128))
    con = db.Column(db.DateTime)
    dremarks = db.Column(db.String(255), nullable=True)
    did = db.Column(db.String(255), nullable=True)
    dkey = db.Column(db.String(255))
    unique_id = db.Column(db.String(255))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, dcode, d_value, efrom, eto, cby,
                 con, dremarks, did, dkey, unique_id, status, created_at, updated_at):
        self.dcode = dcode
        self.d_value = d_value
        self.efrom = efrom
        self.eto = eto
        self.cby = cby
        self.con = con
        self.dremarks = dremarks
        self.did = did
        self.dkey = dkey
        self.unique_id = unique_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def update_by_form_id(_unique_id, _dcode):
        CurrentDatetime = datetime.datetime.now()
        yesterday = CurrentDatetime - datetime.timedelta(days=1)
        print(_unique_id)
        cr_dd.query.filter_by(unique_id=_unique_id, dcode=_dcode, status="active").update({
            cr_dd.status: "inactive", cr_dd.eto: yesterday
        })
        db.session.flush()
        db.session.commit()

    def Add_cr_dd(_dcode, _d_value, _cby, _dremarks, _did, _dkey, _unique_id, _status):
        add_cr_dd = cr_dd(dcode=_dcode, d_value=_d_value, efrom=datetime.datetime.now(),
                          eto=datetime.datetime(9999, 12, 31, 10, 51, 0),
                          cby=_cby, con=datetime.datetime.now(),
                          dremarks=_dremarks, did=_did, dkey=_dkey, unique_id=_unique_id,
                          status=_status, created_at=datetime.datetime.now(), updated_at=None)
        db.session.add(add_cr_dd)
        db.session.commit()
        
    def get_user_demog_value_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="cl_clms_id").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).all()
        demog = cr_dd_schema(many=True)
        output = demog.dump(get_dd)
        return output
        
    def get_user_pass_validity_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="cl_pass_valid_upto").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).all()
        demog = cr_dd_schema(many=True)
        output = demog.dump(get_dd)
        return [each["d_value"] for each in output]
    
    #### vendor labour limit for b1   _unique_id = B1 form
    def get_vendor_labour_limit_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="vd_max_persons_allowed",status="active").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).first()
        demog = cr_dd_schema()
        output = demog.dump(get_dd)
        return int(output.get("d_value"))
    #### vendor b1 form if from b2  _unique_id = B2 form  
    def get_vendor_form_id_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="vd_b1",status="active").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).first()
        demog = cr_dd_schema()
        output = demog.dump(get_dd)
        return output.get("d_value")
        
    def get_cl_job_start_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="cl_job_start_date",status="active").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).first()
        demog = cr_dd_schema()
        output = demog.dump(get_dd)
        return output.get("d_value")
        
    def get_cl_job_end_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="cl_job_end_date",status="active").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).first()
        demog = cr_dd_schema()
        output = demog.dump(get_dd)
        return output.get("d_value")
        
    def get_cl_pfno_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="cl_pfno",status="active").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).first()
        demog = cr_dd_schema()
        output = demog.dump(get_dd)
        return output.get("d_value")
    
    def get_cl_esino_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="cl_esino",status="active").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).first()
        demog = cr_dd_schema()
        output = demog.dump(get_dd)
        return output.get("d_value")
    
    def get_cl_gender_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="cl_gender",status="active").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).first()
        demog = cr_dd_schema()
        output = demog.dump(get_dd)
        return output.get("d_value")
    
    def get_cl_dob_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="cl_dob",status="active").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).first()
        demog = cr_dd_schema()
        output = demog.dump(get_dd)
        return output.get("d_value")
        
    

    def get_user_pcc_validity_by_demog_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode="cl_pcc_validity").with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).all()
        demog = cr_dd_schema(many=True)
        output = demog.dump(get_dd)
        return [each["d_value"] for each in output]
        
    def get_po_value_by_demog_value(_d_value):
        get_dd = cr_dd.query.filter_by(dcode="cl_po", d_value=_d_value).with_entities(cr_dd.unique_id) \
            .order_by(cr_dd.created_at.desc()).all()
        demog = cr_dd_schema(many=True)
        output = demog.dump(get_dd)
        return output
        
    def get_demog_value_by_demog_value( _d_value):
        get_dd = cr_dd.query.filter_by(d_value=_d_value).with_entities(cr_dd.unique_id) \
            .order_by(cr_dd.created_at.desc()).first()
        demog = cr_dd_schema()
        output = demog.dump(get_dd)
        return output

    def get_demog_value_by_demog_id(_unique_id, _dcode):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id, dcode=_dcode).with_entities(cr_dd.d_value) \
            .order_by(cr_dd.created_at.desc()).first()
        demog = cr_dd_schema()
        output = demog.dump(get_dd)
        return output

    def get_dd_by_form_id(_unique_id):
        get_dd = cr_dd.query.filter_by(unique_id=_unique_id).order_by(cr_dd.created_at.desc()).all()
        demog = cr_dd_schema(many=True)
        output = demog.dump(get_dd)
        final_output = []
        for each in output:
            each['user_details'] = Users.FetchUSerDetails_By_employee_id(each["cby"])

        return output


class cr_dd_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = cr_dd


class media_doc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attachment_code = db.Column(db.String(255))
    details = db.Column(db.String(255), nullable=True)
    path = db.Column(db.String(255))
    unique_id = db.Column(db.String(255))
    action_by = db.Column(db.String(255))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, attachment_code, details, path, unique_id, action_by, status, created_at, deleted_at):
        self.attachment_code = attachment_code
        self.details = details
        self.path = path
        self.unique_id = unique_id
        self.action_by = action_by
        self.status = status
        self.created_at = created_at
        self.deleted_at = deleted_at

    def Add_media_doc(_attachment_code, _details, _path, _unique_id, _action_by, _status):
        add_media_cod = media_doc(attachment_code=_attachment_code, details=_details, path=_path, unique_id=_unique_id,
                                  action_by=_action_by, status=_status, created_at=datetime.datetime.now(),
                                  deleted_at=None)
        db.session.add(add_media_cod)
        db.session.commit()

    def get_document_by_form_id(_unique_id):
        get_document = media_doc.query.filter_by(unique_id=_unique_id).all()
        media_docs = media_doc_schema(many=True)
        output = media_docs.dump(get_document)
        final_output = []
        for each in output:
            each['user_details'] = Users.FetchUSerDetails_By_employee_id(each["action_by"])

        return output

    def update_by_form_id(_unique_id, _attachment_code):
        media_doc.query.filter_by(unique_id=_unique_id, attachment_code=_attachment_code, status="active").update({
            media_doc.status: "inactive"
        })
        db.session.flush()
        db.session.commit()


class media_doc_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = media_doc


class Cr_info(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    dept = db.Column(db.String(255))
    yard_no = db.Column(db.String(255))
    init_by = db.Column(db.String(255))
    unit = db.Column(db.String(255))
    po_number = db.Column(db.BigInteger)
    cost_center = db.Column(db.String(255))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    form_id = db.Column(db.String(20))
    unique_id = db.Column(db.String(20))
    state = db.Column(db.String(50))
    form_status = db.Column(db.String(50), nullable=True)
    onboard_by = db.Column(db.String(255), nullable=True)
    onboard_at = db.Column(db.DateTime, nullable=True)
    is_deleted = db.Column(db.Integer, nullable=True)
    designation = db.Column(db.String(50))
    last_updated_by = db.Column(db.String(255), nullable=True)
    remark = db.Column(db.String(255), nullable=True)
    form_state_status = db.Column(db.String(50), nullable=True)
    form_heading = db.Column(db.String(255), nullable=True)
    
    def __init__(self, dept, yard_no, init_by, unit, po_number, cost_center, status, created_at,
                 form_id, unique_id, designation, state, form_status, onboard_by, onboard_at, is_deleted,
                 last_updated_by,remark, form_state_status,form_heading):
        self.dept = dept
        self.yard_no = yard_no
        self.init_by = init_by
        self.unit = unit
        self.po_number = po_number
        self.cost_center = cost_center
        self.status = status
        self.created_at = created_at
        self.form_id = form_id
        self.unique_id = unique_id
        self.designation = designation
        self.state = state
        self.form_status = form_status
        self.onboard_by = onboard_by
        self.onboard_at = onboard_at
        self.is_deleted = is_deleted
        self.last_updated_by = last_updated_by
        self.remark = remark
        self.form_state_status = form_state_status
        self.form_heading = form_heading

    def Add_cr_info(_dept, _yard_no, _init_by, _unit, _po_number, _costcenter, _status, _form_id, _unique_id,
                    _designation, _state, _form_status, _onboard_by, _onboard_at, _is_deleted, _last_updated_by, _remark, _form_state,_form_heading):
        add_cr_info = Cr_info(dept=_dept, yard_no=_yard_no, init_by=_init_by, unit=_unit, po_number=_po_number,
                              cost_center=_costcenter,
                              status=_status, created_at=datetime.datetime.now(), form_id=_form_id,
                              unique_id=_unique_id, designation=_designation, state=_state, form_status=_form_status,
                              onboard_by=_onboard_by, onboard_at=_onboard_at, is_deleted=_is_deleted,
                              last_updated_by=_last_updated_by, remark=_remark, form_state_status=_form_state,form_heading=_form_heading)
        db.session.add(add_cr_info)
        db.session.commit()

    def Fetch_cr_info(_unique_id):
        query = Cr_info.query.filter(Cr_info.unique_id == _unique_id, Cr_info.form_status != "release").order_by(
            Cr_info.created_at.desc()).all()
        CrInfoSchema = cr_info_schema(many=True)
        output = CrInfoSchema.dump(query)
        return output

    def Fetch_cr_info_first(_unique_id):
        query = Cr_info.query.filter_by(unique_id=_unique_id).order_by(Cr_info.created_at).first()
        CrInfoSchema = cr_info_schema()
        output = CrInfoSchema.dump(query)
        return output["init_by"]

    def Fetch_cr_info_asc(_unique_id):
        query = Cr_info.query.filter_by(unique_id=_unique_id).order_by(Cr_info.created_at).all()
        CrInfoSchema = cr_info_schema(many=True)
        output = CrInfoSchema.dump(query)
        return output
        
    def check_cr_form_if_exists_in_po(_po_code):
        query = Cr_info.query.filter(Cr_info.po_number == str(_po_code)).all()
        VendorSchema = cr_info_schema(many=True)
        output = VendorSchema.dump(query)
        if len(output) is 0:
            return False
        else:
            return True
            
    def Fetch_revision(_init_by, _unique_id):
        search_query2 = f"SELECT * FROM cr_info WHERE last_updated_by IN ('{_init_by}') and unique_id IN ('{_unique_id}')"
        query=db.session.execute(search_query2)
        CrInfoSchema = cr_info_schema(many=True)
        output = CrInfoSchema.dump(query)
        return output
    
    def Fetch_cr_info_po(_po_code):
        query = Cr_info.query.filter(Cr_info.po_number == str(_po_code)).all()
        VendorSchema = cr_info_schema(many=True)
        output = VendorSchema.dump(query)
        return [each["unique_id"] for each in output]

    def update_by_form_id(_unique_id, status, _is_deleted=0):
        Cr_info.query.filter_by(unique_id=_unique_id, is_deleted=0).update({
            Cr_info.status: status, Cr_info.is_deleted: _is_deleted,
        })
        db.session.flush()
        db.session.commit()


class cr_info_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cr_info
        
class Blacklist_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alpeta_id = db.Column(db.Integer)
    block_from = db.Column(db.DateTime, nullable=True)
    block_to = db.Column(db.DateTime, nullable=True)
    user_terminal_id = db.Column(db.Integer)
    terminal_id = db.Column(db.String(20))
    user_id = db.Column(db.String(20))
    executed = db.Column(db.Integer)
    processing = db.Column(db.Integer)
    is_block = db.Column(db.Integer)
    status = db.Column(db.String(10))
    execution_status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    executed_at = db.Column(db.DateTime)

    def __init__(self, alpeta_id, block_from, block_to, user_terminal_id, terminal_id, user_id,
                 executed, processing, is_block, execution_status, status, created_at, executed_at):
        self.alpeta_id = alpeta_id
        self.block_from = block_from
        self.block_to = block_to
        self.user_terminal_id = user_terminal_id
        self.terminal_id = terminal_id
        self.user_id = user_id
        self.executed = executed
        self.processing = processing
        self.is_block = is_block
        self.status = status
        self.execution_status = execution_status
        self.created_at = created_at
        self.executed_at = executed_at

    def AddBlacklist(_alpeta_id, _user_terminal_id, _terminal_id, _user_id, _executed,
                     _processing, _is_block, _execution_status, _executed_at):
        add_blacklist = Blacklist_request(alpeta_id=_alpeta_id,
                                          block_from=datetime.datetime.now(),
                                          block_to=datetime.datetime(2099, 1, 1, 0, 0, 00, 00),
                                          user_terminal_id=_user_terminal_id,
                                          terminal_id=_terminal_id,
                                          user_id=_user_id,
                                          executed=_executed,
                                          processing=_processing,
                                          is_block=_is_block,
                                          status="active",
                                          execution_status=_execution_status,
                                          created_at=datetime.datetime.now(),
                                          executed_at=_executed_at
                                          )
        db.session.add(add_blacklist)
        db.session.commit()

    def update_blacklist(_user_id, _terminal_id, _executed, _processing, _is_block, _execution_status, _executed_at):
        Blacklist_request.query.filter_by(user_id=_user_id, terminal_id=_terminal_id, status="active").update({
            Blacklist_request.executed: _executed,
            Blacklist_request.processing: _processing,
            Blacklist_request.is_block: _is_block,
            Blacklist_request.executed_at: _executed_at,
            Blacklist_request.execution_status: _execution_status
        })
        db.session.flush()
        db.session.commit()

    def Fetch_update_blacklist(_user_id, _terminal_id):
        query = Blacklist_request.query.filter_by(user_id=_user_id, terminal_id=_terminal_id, status="active").first()
        BlacklistRequestSchema = Blacklist_request_schema()
        output = BlacklistRequestSchema.dump(query)
        return output

    def update_status_blacklist(_id):
        Blacklist_request.query.filter_by(id=_id, status="active").update(
            {Blacklist_request.status: "inactive"})
        db.session.flush()
        db.session.commit()


class Blacklist_request_schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist_request

