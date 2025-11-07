from flask import Flask, jsonify, request,session,send_from_directory
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
import json,random,csv,io,ast
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from emailer import send_templated_email




app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'labguard'
app.config['SECRET_KEY'] = 'labguardsecretkey'
CORS(app, origins="*",supports_credentials=True)
mysql = MySQL(app)

current_user = None


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/upload_profile_image", methods=["POST"])
@cross_origin(supports_credentials=True)
def upload_profile_image():
    global current_user
    if not current_user:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    if "image" not in request.files:
        return jsonify({"success": False, "message": "No file uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400

 
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE users SET profile=%s WHERE lgid=%s",
        (filename, current_user['lgid'])
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"success": True, "image_url": f"{filename}"})


@app.route("/update_profile", methods=["POST"])
@cross_origin(supports_credentials=True)
def update_profile():
    global current_user
    if not current_user:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    department = data.get("department")
    position = data.get("position")
    new_password = data.get("newPassword")
    current_password = data.get("currentPassword")
    image_filename = data.get("image")  

    if image_filename and "/" in image_filename:
        image_filename = image_filename.split("/")[-1]

    cursor = mysql.connection.cursor()

    if new_password:
        cursor.execute("SELECT password FROM users WHERE lgid=%s", (current_user['lgid'],))
        stored_pw = cursor.fetchone()[0]
        if stored_pw != current_password:
            cursor.close()
            return jsonify({"success": False, "message": "Current password is incorrect"}), 401

        cursor.execute(
            "UPDATE users SET password=%s WHERE lgid=%s",
            (new_password, current_user['lgid'])
        )

    cursor.execute(
        "UPDATE users SET name=%s, email=%s, department=%s, position=%s, profile=%s WHERE lgid=%s",
        (name, email, department, position, image_filename, current_user['lgid'])
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"success": True, "message": "Profile updated successfully"})


@app.route("/get_user")
@cross_origin(supports_credentials=True)
def get_user():
    global current_user
    if not current_user:
        return jsonify({"error": "Not logged in"}), 401

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT lgid, name, email, role, year, password, profile, department, position "
        "FROM users WHERE lgid=%s",
        (current_user['lgid'],)
    )
    profile = cursor.fetchone()
    cursor.close()

    if profile:
        filename = profile[6]  
        if filename:
            image_url = f"http://127.0.0.1:5000/uploads/{filename}"
        else:
            image_url = "/img/default.png"

        userProfile = {
            "lgid": profile[0],
            "name": profile[1],
            "email": profile[2],
            "role": profile[3],
            "year": profile[4],
            "password": profile[5],
            "image": image_url,
            "department": profile[7],
            "position": profile[8],
        }
        return jsonify(userProfile)

    return jsonify({"error": "User not found"}), 404



@app.route('/delete_user/<email>', methods=['DELETE'])
def delete_user(email):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        mysql.connection.commit()
        cursor.close()
        return {"message": f"User with email {email} deleted successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
@app.route('/delete_report/<id>', methods=['DELETE'])
def delete_report(id):
    if id == "ALL":
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM reports")
            mysql.connection.commit()
            cursor.close()
            return {"message": f"Deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    else:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM reports WHERE id = %s", (id,))
            mysql.connection.commit()
            cursor.close()
            return {"message": f"Deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
@app.route('/delete_lab/<string:lab_name>', methods=['DELETE'])
def delete_lab(lab_name):
    try:
        print("Lab Name to delete:", lab_name)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM computer_equipments WHERE lab_name = %s", (lab_name,))
        
        computer_ids = [row[0] for row in cursor.fetchall()]
        for com_id in computer_ids:
            cursor.execute("DELETE FROM computer_status WHERE com_id = %s", (com_id,))
            cursor.execute("DELETE FROM reports WHERE com_id = %s", (com_id,))
            cursor.execute("DELETE FROM other_part_status WHERE com_id = %s", (com_id,))

        cursor.execute("DELETE FROM computer_equipments WHERE lab_name = %s", (lab_name,))

        cursor.execute("DELETE FROM laboratory WHERE lab_name = %s", (lab_name,))

        mysql.connection.commit()
        cursor.close()

        return {"message": f"Lab '{lab_name}' and all related records deleted"}, 200

    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}, 500
@app.route('/delete_computer/<string:id>', methods=['DELETE'])
def delete_computer(id):
    try:
        print("Computer ID to delete: ",id)
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM computer_equipments WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.execute("DELETE FROM computer_status WHERE com_id = %s", (id,))
        mysql.connection.commit()
        cursor.execute("DELETE FROM reports WHERE com_id = %s", (id,))
        mysql.connection.commit()
        cursor.execute("DELETE FROM other_part_status WHERE com_id = %s", (id,))
        mysql.connection.commit()
        print("Deleted computer with ID: ",id)
        return {"message": "Lab deleted"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/edit_lab/<lab_id>", methods=["PUT"])
def edit_lab(lab_id):
    try:
        data = request.get_json()
        print(data)
        new_lab_name = data.get("lab_name")
        location = data.get("location")

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE laboratory SET lab_name=%s, location=%s WHERE lab_id=%s",
            (new_lab_name, location, lab_id)
        )
        mysql.connection.commit()
        cursor.execute(
            "UPDATE computer_equipments SET lab_name=%s WHERE lab_id=%s",
            (new_lab_name, lab_id)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({"success": True, "message": "Lab updated successfully"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    global current_user
    try:
        data = request.json.get('data')
        email = data.get('email')
        password = data.get('password')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT lgid, name, email, role, year, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if not user:
            return jsonify({"msg": "User not found"}), 404

        user_id, name, email, role, year, stored_pw = user

        if stored_pw != password:
            return jsonify({"msg": "Invalid credentials"}), 401
        
        current_user = {
            "lgid": user_id,
            "name": name,
            "email": email,
            "role": role,
            "year": year
        }

        return jsonify({
            "msg": "Login successful",
            "user": {
                "lgid": user_id,
                "name": name,
                "email": email,
                "role": role, 
                "year": year
            }
        }), 200
    except Exception as e:
        print("Error in login:", e)
        return jsonify({"msg": str(e)}), 500

@app.route('/add_report', methods=['POST'])
@cross_origin()
def add_report():
    
    email = request.headers.get("X-User-Email")
    report = request.json.get('data')
    print(report)
    lab = report['lab']
    item = report['item']
    label = report['label']
    quantity = report['quantity']
    status = report['status']
    notes = report['notes']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO reports (lab,item,quantity,status,notes,submitted_by,label) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                   ( lab, item, quantity, status, notes, email,label))
    mysql.connection.commit()
    cursor.close()

    return {"report": "added succesfully"}




    

@app.route('/add_laboratory', methods=['POST'])
def add_laboratory():
    data = request.json.get('data')

    lab_name = data.get('lab_name')
    location = data.get('location')

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT lab_name FROM laboratory WHERE lab_name = %s",(lab_name,))
    existing_lab = cursor.fetchone()
    if existing_lab:
        return {"error": "Laboratory with this name already exists."}, 400

    cursor.execute("INSERT INTO laboratory (lab_name, location) VALUES (%s,%s)",(lab_name,location,))
    mysql.connection.commit()

    new_id = cursor.lastrowid


    return {
        "id": new_id,
        "name": lab_name,
        "location": location
    }

@app.route('/get_data')
def get_data():
    cursor = mysql.connection.cursor()

    # --- Fetch tables ---
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()  # user_id, name, ..., has_voted

    cursor.execute("SELECT * FROM laboratory")
    laboratories = cursor.fetchall()  # lab_id, lab_name, location

    cursor.execute("SELECT * FROM computer_equipments")
    computer_equipments = cursor.fetchall()  # id, lab_name, pc_name

    cursor.execute("SELECT * FROM computer_status")
    computer_status = cursor.fetchall()  # com_id, hdmi, headphone, keyboard, monitor, mouse, power, systemUnit, wifi, status_id

    cursor.execute("SELECT * FROM reports")
    reports = cursor.fetchall()  # id, user_id, com_id, date, notes

    cursor.execute("SELECT * FROM other_part_status")
    other_part_status_fetch = cursor.fetchall()


    other_part_status = []
    for row in other_part_status_fetch:
        # Assuming columns: (com_id, parts, status_id)
        parts_data = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        other_part_status.append({
            'com_id': row[0],
            'parts': parts_data,
            'status_id': row[2] if len(row) > 2 else None
        })

    # --- Counting variables with "other_" prefix ---
    other_total = 0
    other_operational = 0
    other_not_operational = 0
    other_damaged = 0
    other_missing = 0

    # --- Count all statuses ---
    for record in other_part_status:
        for status in record['parts'].values():
            other_total += 1
            val = str(status).lower()
            if val == 'operational':
                other_operational += 1
            elif val == 'notoperational':
                other_not_operational += 1
            elif val == 'damaged':
                other_damaged += 1
            elif val == 'missing':
                other_missing += 1

    # --- Final dictionary ---
    otherPartStatus = {
        "total": other_total,
        "operational": other_operational,
        "notOperational": other_not_operational,
        "damaged": other_damaged,
        "missing": other_missing
    }

    print("otherPartStatus",otherPartStatus)
    

    # --- Summary stats ---
    total_users = len(users)
    active_users = sum(1 for u in users if u[4] not in ("0", None))  # adjust index for has_voted
    inactive_users = total_users - active_users

    total_labs = len(laboratories)
    total_computers = len(computer_equipments)

    # Overall operational stats
    operational = not_operational = damaged = missing = 0
    for status in computer_status:
        for s in status[1:9]:  # exclude com_id and status_id
            val = str(s).lower()
            if val == "operational":
                operational += 1
            elif val == "notoperational":
                not_operational += 1
            elif val == "damaged":
                damaged += 1
            elif val == "missing":
                missing += 1

    reports_submitted = len(reports)

    # --- Computer parts status ---
    parts = ["wifi","headphone","keyboard","hdmi","monitor","mouse","power","systemUnit"]
    computerPartStatus = []
    for i, part in enumerate(parts):
        operational_count = sum(1 for row in computer_status if str(row[i+1]).lower() == "operational")
        not_op_count = sum(1 for row in computer_status if str(row[i+1]).lower() == "notoperational")
        damaged_count = sum(1 for row in computer_status if str(row[i+1]).lower() == "damaged")
        missing_count = sum(1 for row in computer_status if str(row[i+1]).lower() == "missing")
        computerPartStatus.append({
            "name": part,
            "operational": operational_count,
            "notOperational": not_op_count,
            "damaged": damaged_count,
            "missing": missing_count
        })

    # --- Labs & Computers and Damage vs Missing ---
    labEquipments = []
    damageMissing = []

    for lab in laboratories:
        lab_id, lab_name, location = lab
        total = sum(1 for comp in computer_equipments if comp[1] == lab_name)
        damaged_count = 0
        missing_count = 0
        for comp in computer_equipments:
            if comp[1] == lab_name:
                comp_id = comp[3]
                for status in computer_status:
                   
                    if status[0] == comp_id:
                        vals = [str(x).lower() for x in status[1:9]]
                        damaged_count += vals.count("damaged")
                        missing_count += vals.count("missing")

        # Use "name" as key to match React
        labEquipments.append({
            "name": lab_name,
            "computers": total
        })

        damageMissing.append({
            "name": lab_name,
            "damaged": damaged_count,
            "missing": missing_count
        })

    cursor.close()

    # --- Print debug info ---
    print("labEquipments:", labEquipments)
    print("damageMissing:", damageMissing)

    return jsonify({
        "stats": {
            "totalLabs": total_labs,
            "totalComputers": total_computers,
            "operational": operational,
            "notOperational": not_operational,
            "totalUsers": total_users,
            "activeUsers": active_users,
            "inactiveUsers": inactive_users,
            "reportsSubmitted": reports_submitted,
            "damaged": damaged,
            "missing": missing,
        },
        "computerPartStatus": computerPartStatus,
        "labEquipments": labEquipments,
        "damageMissing": damageMissing,
        "otherPartStatus":otherPartStatus
    })

@app.route('/get_laboratory', methods=['GET'])
def get_laboratory():
    final_data = []
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM laboratory")
    data = cursor.fetchall()

    for i in data:
        labs = {
            "lab_id": i[0],
            "name" : i[1],
            "location" : i[2]
        }

        final_data.append(labs)

    return final_data

@app.route('/update_computer_status_bulk', methods=['POST'])
def update_computer_status_bulk():
    data = request.json
    all_statuses = data.get("statuses", {})

    if not all_statuses:
        return jsonify({"error": "No statuses provided"}), 400

    cursor = mysql.connection.cursor()
    try:
        valid_parts = ["monitor", "systemUnit", "keyboard", "mouse", "headphone", "hdmi", "power", "wifi"]

        for comp_id_str, parts in all_statuses.items():
            comp_id = int(comp_id_str)  
            for part, status in parts.items():
                if part not in valid_parts:
                    continue
                query = f"UPDATE computer_status SET {part} = %s WHERE com_id = %s"
                cursor.execute(query, (status, comp_id))

        mysql.connection.commit()
        return jsonify({"success": True, "message": "All selected PCs updated!"})

    except Exception as e:
        print("Error updating PCs:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@app.route('/get_computers', methods=['GET'])
def get_computers():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, pc_name, lab_name, specs FROM computer_equipments")
        rows = cur.fetchall()
        cur.close()

        computers = []
        for row in rows:
            computers.append({
                "id": row[0],
                "pcNumber": row[1],
                "lab": row[2],
                "parts": json.loads(row[3]) if row[3] else {}
            })

        

        return jsonify(computers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_computer_statuses')
def get_computer_statuses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM computer_status")
    rows = cur.fetchall()
    cur.close()

    statuses = []
    for row in rows:
        statuses.append({
            "com_id": row[0],
            "hdmi": row[1],
            "headphone": row[2],
            "keyboard": row[3],
            "monitor": row[4],
            "mouse": row[5],
            "power": row[6],
            "systemUnit": row[7],
            "wifi": row[8],
            "status_id": row[9]
        })

    return jsonify(statuses)
        
@app.route('/get_other_part_status')
def get_other_part_status():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM other_part_status")
    rows = cur.fetchall()
    cur.close()

    parts_status = []
    for row in rows:
        parts_status.append({
            "com_id": row[0],
            "parts": json.loads(row[1]) if row[1] else {},
            "status_id": row[2]
        })

    return jsonify(parts_status)
    
    

@app.route('/update_computer_status', methods=['POST'])
def update_status():
    data = request.json
    
    comp_id = data.get("compId")
    statuses = data.get("statuses", {})
    compOtherParts = data.get("compOtherParts",{})

    cursor = mysql.connection.cursor()

    for part, status in statuses.items():
        query = f"UPDATE computer_status SET {part} = %s WHERE com_id = %s"
        cursor.execute(query, (status, comp_id))
        mysql.connection.commit()
        if status == 'operational':
            cursor.execute("DELETE FROM reports WHERE com_id = %s AND notes = %s",(comp_id,f"{part} issue detected"))
            mysql.connection.commit()

    for part_id, status in compOtherParts.items():
        print(part_id,status)

        cursor.execute("UPDATE other_part_status set parts = JSON_SET(parts, %s, %s) WHERE com_id = %s",(f"$.{part_id}",status,comp_id))
        mysql.connection.commit()
        if status == 'operational':
            print(status,f"Other part {part} issue detected" )
            cursor.execute("DELETE FROM reports WHERE com_id = %s AND notes = %s",(comp_id,f"Other part {part_id} issue detected"))
            mysql.connection.commit()

    
    cursor.close()
    return jsonify({"success": True})



      
    



@app.route('/get_admin_computer_reports')
def get_admin_computer_reports():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM computer_status")
    rows = cur.fetchall()
    # cur.execute("DELETE FROM reports WHERE 1")
    # mysql.connection.commit()

    reports = []
    for row in rows:
        com_id, hdmi, headphone, keyboard, monitor, mouse, power, systemUnit, wifi, status_id = row

        parts = {
            "hdmi": hdmi,
            "headphone": headphone,
            "keyboard": keyboard,
            "monitor": monitor,
            "mouse": mouse,
            "power": power,
            "systemUnit": systemUnit,
            "wifi": wifi,
        }

        for part, status in parts.items():
            if status != "operational":
                cur.execute(
                    "SELECT lab_name, pc_name FROM computer_equipments WHERE id = %s",
                    (com_id,)
                )
                result = cur.fetchone()
                if not result:
                    continue
                lab_name, pc_name = result
                notes = f"{part} issue detected"

                # Check if the report already exists
                cur.execute(
                    "SELECT id, status, created_at, sent FROM reports WHERE com_id = %s AND notes = %s",
                    (com_id, notes)
                )
                report_fetch = cur.fetchone()

                if report_fetch:
                    report_id, status_text, created_at, sent = report_fetch
                else:
                    # Insert new report
                    created_at = datetime.now()
                    sent = 0  # Default to 0 (not sent)
                    cur.execute(
                        """
                        INSERT INTO reports (com_id, lab, status, created_at, notes, sent)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (com_id, lab_name, status.capitalize(), created_at, notes, sent)
                    )
                    mysql.connection.commit()
                    report_id = cur.lastrowid
                    status_text = status.capitalize()

                # Append to response
                reports.append({
                    "id": report_id,
                    "item": pc_name,
                    "lab": lab_name,
                    "status": status_text,
                    "date": created_at.isoformat(),
                    "notes": notes,
                    "sent": sent
                })

        cur.execute("SELECT parts FROM other_part_status WHERE com_id = %s", (com_id,))
        result = cur.fetchone()
        if not result:
            continue

        other_parts_json = result[0]
        if not other_parts_json:
            continue

        try:
            other_parts = json.loads(other_parts_json)
        except json.JSONDecodeError:
            continue

        for part, status in other_parts.items():
            print("looking at other part:", part, status,other_parts)
            if status != "operational":
                cur.execute(
                    "SELECT lab_name, pc_name FROM computer_equipments WHERE id = %s",
                    (com_id,)
                )
                result = cur.fetchone()
                if not result:
                    continue
                lab_name, pc_name = result
                notes = f"Other part {part} issue detected"

                cur.execute(
                    "SELECT id, status, created_at, sent FROM reports WHERE com_id = %s AND notes = %s",
                    (com_id, notes)
                )
                report_fetch = cur.fetchone()

                if report_fetch:
                    report_id, status_text, created_at, sent = report_fetch
                else:
                    created_at = datetime.now()
                    sent = 0
                    cur.execute(
                        """
                        INSERT INTO reports (com_id, lab, status, created_at, notes, sent)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (com_id, lab_name, status.capitalize(), created_at, notes, sent)
                    )
                    mysql.connection.commit()
                    report_id = cur.lastrowid
                    status_text = status.capitalize()

                reports.append({
                    "id": report_id,
                    "item": f"{pc_name}",
                    "lab": lab_name,
                    "status": status_text,
                    "date": created_at.isoformat(),
                    "notes": notes,
                    "sent": sent
                })
    

    
        

    cur.close()
    # Sort by date descending
    reports.sort(key=lambda x: datetime.fromisoformat(x["date"]), reverse=True)
    return jsonify(reports)





@app.route('/get_accessories', methods=["GET"])
def get_accessories():
    final_data = []
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM accessories_equipment")
    data = cursor.fetchall()

    for i in data:
        computer = {
            "id" : i[2],
            "name" : i[3],
            "spec" : i[0],
            "lab" : i[1]
        }

        final_data.append(computer)

    return final_data

@app.route('/add_accessories', methods=["POST"])
def add_accessories():
    data = request.json.get('data')
    
    name = data.get('name')
    lab_name = data.get('lab_name')
    spec = data.get('spec')
    cursor = mysql.connection.cursor()

    cursor.execute("INSERT INTO accessories_equipment (spec,lab,name) VALUES (%s,%s,%s)",(spec,lab_name,name))
    mysql.connection.commit()

    return "success"

@app.route("/labs-pc-count", methods=["GET"])
def labs_pc_count():
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT lab_name, COUNT(pc_name) FROM computer_equipments GROUP BY lab_name"
        )
        rows = cur.fetchall()
        cur.close()
        lab_counts = [{"lab_name": lab, "count": count} for lab, count in rows]
        
        return jsonify(lab_counts)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/computer', methods=['POST'])
def add_computer():
    try:
        data = request.json.get('data')
        lab_id = data.get('id')
        other_parts = json.loads(data.get('other_parts'))
        pc_name = data.get('name')
        lab_name = data.get('lab_name')
        spec = data.get('spec')

        parts = {}
        parts_status = {}

        for other in other_parts:
            parts[other['name']] = other['serial']

        for other in other_parts:
            parts_status[other['name']] = 'operational'

        random_id = str(random.randint(11111111, 99999999))
        status_id = str(random.randint(11111111, 99999999))

        cur = mysql.connection.cursor()

        # ✅ Check if the same PC name already exists in the same lab
        cur.execute(
            "SELECT COUNT(*) FROM computer_equipments WHERE lab_name = %s AND pc_name = %s",
            (lab_name, pc_name)
        )
        exists = cur.fetchone()[0]
        if exists > 0:
            cur.close()
            return jsonify({"error": f"Computer name '{pc_name}' already exists in lab '{lab_name}'."}), 400

        other_final = json.dumps(parts)
        status_final = json.dumps(parts_status)
        print(other_final)
        cur.execute(
            "INSERT INTO computer_equipments (pc_name, lab_name, specs, id,lab_id,other_parts) VALUES (%s, %s, %s, %s,%s,%s)",
            (pc_name, lab_name, spec, random_id,lab_id,str(other_final))
        )
        
        mysql.connection.commit()

        cur.execute(
            "INSERT INTO computer_status (com_id, status_id) VALUES (%s, %s)",
            (random_id, status_id)
        )
        print(parts_status)
        mysql.connection.commit()
        cur.execute(
            "INSERT INTO other_part_status (com_id,parts,status_id) VALUES (%s,%s, %s)",
            (random_id,str(status_final) ,status_id)
        )
        mysql.connection.commit()

        cur.close()

        return jsonify({
            "id": random_id,
            "pcNumber": pc_name,
            "lab": lab_name,
            "parts": json.loads(spec)
        })

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/computer/bulk', methods=['POST'])
def computer_bulk():
    data = request.json.get('data')
    inserted_computers = []
    skipped = []

    for computer in data:
        try:
            pc_name = computer['pc_name']
            lab_name = computer['lab_name']
            spec = computer['specs']

            cur = mysql.connection.cursor()

            # ✅ Skip duplicates
            cur.execute(
                "SELECT COUNT(*) FROM computer_equipments WHERE lab_name = %s AND pc_name = %s",
                (lab_name, pc_name)
            )
            exists = cur.fetchone()[0]
            if exists > 0:
                skipped.append(pc_name)
                cur.close()
                continue

            id = str(random.randint(11111111, 99999999))
            cur.execute(
                "INSERT INTO computer_equipments (pc_name, lab_name, specs, id) VALUES (%s, %s, %s, %s)",
                (pc_name, lab_name, spec, id)
            )
            mysql.connection.commit()

            id_status = str(random.randint(11111111, 99999999))
            cur.execute(
                "INSERT INTO computer_status (com_id, status_id) VALUES (%s, %s)",
                (id, id_status)
            )
            mysql.connection.commit()

            cur.close()

            inserted_computers.append({
                "id": id,
                "pcNumber": pc_name,
                "lab": lab_name,
                "parts": json.loads(spec)
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({
        "inserted": inserted_computers,
        "skipped_duplicates": skipped
    })

@app.route('/send_report_email', methods=['POST'])
def send_report_email():
    cur = mysql.connection.cursor()
    
    title = request.json.get('title')
    summary = request.json.get('summary')
    position = request.json.get('position')
    userEmail = request.json.get('userEmail')
    
    context = {
        "title": title,
        "summary": summary,
        "recipient": [
            "nama.alarcom.ui@phinmaed.com"
        ],
        "position": position,
        "userEmail": userEmail
    }

    # Send the email
    send_templated_email(
        sender_email='claims.pui@gmail.com',
        sender_password='vxdk puti kyhc mdkr',
        receiver_email=context['recipient'],
        subject=f"System Report - {context['title']}",
        template_name='report.html',
        context=context
    )

    # Update reports as sent
    for item in summary:
        cur.execute(
            "UPDATE reports SET sent = 1 WHERE id = %s",
            (item['com_id'],)
        )
        mysql.connection.commit()

    return {"message": "Email sent successfully"}

    
@app.route('/submit_technician_report', methods=['POST'])
def submit_technician_report():
    report_id = request.json.get('report_id')
    issue_found = request.json.get('issue_found')
    solution = request.json.get('solution')
    status = request.json.get('status')
    technician_email = request.json.get('technician_email')
    replacement_serial = request.json.get('replacement_serial')
    part = issue_found['notes'].split()[0]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM computer_equipments WHERE lab_name = %s AND pc_name = %s",(issue_found['lab'],issue_found['PC_Number']))
    com_id = cur.fetchone()[3]
    print(report_id,issue_found,solution,status,technician_email,part,replacement_serial,com_id)
    fix_id = str(random.randint(11111111,99999999))
    cur.execute("INSERT INTO technician_logs (report_id, fix_id, issue_found, solution, status, technician_email) VALUES (%s,%s,%s,%s,%s,%s)",(report_id,fix_id,issue_found,solution,status,technician_email))
    mysql.connection.commit()
    print("DOne1")

    try:
        cur.execute(f"UPDATE computer_status set {part} = %s WHERE com_id = %s",(status,com_id))
        mysql.connection.commit()
    except Exception as e:
        print("Force to other")
        other_part = issue_found['notes'].split()[2]
        cur.execute("UPDATE other_part_status SET parts = JSON_SET(parts,%s,%s) WHERE com_id = %s ", (f"$.{other_part}",status,com_id))
        mysql.connection.commit()

    print("DOne2")
    print(report_id,issue_found['notes'])
    cur.execute("DELETE FROM reports WHERE id = %s AND notes = %s",(report_id,issue_found['notes']))
    mysql.connection.commit()

    print("DOne3")

    if solution == "Replaced" and part != "Other":
        cur.execute("UPDATE computer_equipments set specs = JSON_SET(specs, %s, %s) WHERE lab_name = %s AND pc_name = %s",(f"$.{part}",replacement_serial,issue_found['lab'],issue_found['PC_Number']))
        mysql.connection.commit()

    elif solution == "Replaced" and part == "Other":
        other_part = issue_found['notes'].split()[2]
        cur.execute("UPDATE computer_equipments set other_parts = JSON_SET(other_parts, %s, %s) WHERE lab_name = %s AND pc_name = %s",(f"$.{other_part}",replacement_serial,issue_found['lab'],issue_found['PC_Number']))
        mysql.connection.commit()
    print("DOne4")
    print({
        "report_id": report_id,
        "issue_found": issue_found,
        "solution": solution,
        "status": status,
        "technician_email": technician_email,
        "part": part
    })
    return {"message": "report submitted successfully"}

@app.route('/get_technician_logs')
def get_technician_logs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM technician_logs")
    rows = cur.fetchall()
    cur.close()

    logs = []
    for row in rows:
        issue = ast.literal_eval(row[2])
        logs.append({
            "report_id": row[0],
            "fix_id": row[1],
            "issue_found":issue,
            "solution": row[3],
            "status": row[4],
            "technician_email": row[5],
            "timestamp": row[6].isoformat(),
             "sent": row[7]
             
        })

    return jsonify(logs)


@app.route('/technician_send_report_email', methods=['POST'])
def technician_send_report_email():
    data = request.json.get('data')
    print(data)
    context = {
        "title": data['title'],
        "summary": data['issue_report'],
        'recipient': ["nama.alarcon.ui@phinmaed.com"],
        "position": data['position'],
        "userEmail": data['userEmail']
    }

    send_templated_email(
        sender_email='claims.pui@gmail.com',
        sender_password='vxdk puti kyhc mdkr',
        receiver_email=context['recipient'],
        subject=f"Technician Logs - {context['title']}",
        template_name='technician.html',
        context=context
    )

    # Update the technician logs as sent
    report_ids = [item['report_id'] for item in data['issue_report']]
    
    if report_ids:
        try:
            cursor = mysql.connection.cursor()
            format_strings = ','.join(['%s'] * len(report_ids))
            query = f"UPDATE technician_logs SET sent = 1 WHERE report_id IN ({format_strings})"
            cursor.execute(query, tuple(report_ids))
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Error updating sent status: {e}")
            return {"message": "Error updating logs", "error": str(e)}, 500

    return {"message": "Email sent successfully and logs updated"}


@app.route("/get_edit_data/")
def get_edit_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM computer_equipments")
    rows = cur.fetchall()

    statuses = []
    for row in rows:
        statuses.append({
            "pc_name": row[0],
            "lab_name": row[1],
            "specs": json.loads(row[2]) if row[2] else [],  # Safely handle None
            "id": row[3],
            "lab_id": row[4],
            "other_parts": json.loads(row[5]) if row[5] else [],  # Safely handle None
        })

    return jsonify(statuses)


@app.route("/update_edit_data/<pc_id>", methods=["POST"])
def update_edit_data(pc_id):
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        print("Received edit data:", data,pc_id)

        pc_name = data.get("pcNumber")
        specs = data.get("parts", {})
        other_parts_list = data.get("otherParts", [])

        other_parts_dict = {
            item["name"]: item["serial"]
            for item in other_parts_list
            if item.get("name") and item.get("serial")
        }
        
        


        cur.execute("""
            UPDATE computer_equipments
            SET pc_name = %s,
                specs = %s,
                other_parts = %s
            WHERE id = %s
        """, (
            pc_name,
            json.dumps(specs),
            json.dumps(other_parts_dict),
            pc_id
        ))

        mysql.connection.commit()

        cur.execute("SELECT * FROM other_part_status WHERE com_id = %s", (pc_id,))
        row = cur.fetchone()
        print("Fetched other_part_status row:", row)


        if row:

            fetch_status = json.loads(row[1])
            values = list(fetch_status.values())
            
            print("Fetched other_part_status row:", fetch_status)
            print("Values",values)
            print("other_parts_dict",other_parts_dict)
            
            updated_status = {k: values[i] if i < len(values) else 'operational' 
                            for i, k in enumerate(other_parts_dict.keys())}

            cur.execute("""
                UPDATE other_part_status
                SET parts = %s
                WHERE com_id = %s
            """, (json.dumps(updated_status), pc_id))
            mysql.connection.commit()

            print(updated_status)

        cur.close()

        print(f"✅ Updated PC {pc_id} successfully.")
        return jsonify({"message": "Computer info updated successfully!"}), 200

    except Exception as e:
        print("❌ Error updating computer:", e)
        return jsonify({"error": str(e)}), 500
    

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    lgid = random_id = str(random.randint(11111111, 99999999))
    name = data.get('name')
    email = data.get('email')
    role = data.get('role')
    year = data.get('year')
    password = data.get('password') 
    profile = data.get('profile')
    department = data.get('department')
    position = data.get('position')

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO users (lgid, name, email, role, year, password, profile, department, position)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (lgid, name, email, role, year, password, profile, department, position))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"success": True})


@app.route('/get_users')
def get_users():
    final = []
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    for each in data:
        user = {

            'lgid':each[0],
            'name':each[1],
            'email':each[2],
            'role':each[3],
            'year':each[4],
            'password':each[5],
            'profile':each[6],
            'department':each[7],
            'position':each[8],

        }
        final.append(user)

    return final

@app.route('/users/<string:lgid>', methods=['PUT'])
def update_user(lgid):
    
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role')
    department = request.form.get('department')
    position = request.form.get('position')

    print(type(lgid))
    profile = request.files.get('profile')
    filename = None
    if profile:
        filename = secure_filename(profile.filename)
        path = os.path.join('uploads', filename)
        profile.save(path)

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE users
        SET name=%s, email=%s, role=%s, department=%s, position=%s, profile=%s
        WHERE lgid=%s
    """, (name, email, role, department, position, filename, lgid))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<string:lgid>', methods=['DELETE'])
def delete_userr(lgid):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE lgid = %s", (lgid,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': f'User {lgid} deleted successfully'})


@app.route("/check_session")
def check_session():
    global current_user
    if current_user:
        print("Current user:",current_user)
        return {"logged_in": True, "user": current_user}
    return {"logged_in": False}
    
@app.route("/logout")
def logout():
    global current_user
    current_user = None
    session.pop("user", None)
    return {"message": "Logged out"}



if __name__ == '__main__':
    app.run(debug=True)
