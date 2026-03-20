from fastapi import FastAPI, Response
from pydantic import BaseModel, Field
from typing import Optional
import math

app = FastAPI()

# -----------------------
# DATA
# -----------------------
plans = [
    {"id": 1, "name": "Basic", "duration": 1, "price": 1000, "includes_classes": False, "includes_trainer": False},
    {"id": 2, "name": "Standard", "duration": 6, "price": 5000, "includes_classes": True, "includes_trainer": False},
    {"id": 3, "name": "Premium", "duration": 12, "price": 10000, "includes_classes": True, "includes_trainer": True},
]

memberships = []
membership_counter = 1

class_bookings = []
booking_counter = 1

# -----------------------
# MODELS
# -----------------------
class EnrollRequest(BaseModel):
    member_name: str
    plan_id: int
    phone: str
    start_month: str
    payment_mode: str = "cash"
    referral_code: str = ""

class ClassBooking(BaseModel):
    member_name: str
    class_name: str
    class_date: str

class NewPlan(BaseModel):
    name: str = Field(min_length=2)
    duration_months: int = Field(gt=0)
    price: int = Field(gt=0)
    includes_classes: bool = False
    includes_trainer: bool = False

# -----------------------
# HELPERS
# -----------------------
def find_plan(plan_id):
    return next((p for p in plans if p["id"] == plan_id), None)

def calculate_fee(base_price, duration):
    if duration >= 12:
        return base_price * 0.8
    elif duration >= 6:
        return base_price * 0.9
    return base_price

# -----------------------
# HOME
# -----------------------
@app.get("/")
def home():
    return {"message": "Welcome to IronFit Gym"}

# -----------------------
# MEMBERSHIP (Q6–Q9)
# -----------------------
@app.post("/memberships")
def create_membership(req: EnrollRequest):
    global membership_counter

    plan = find_plan(req.plan_id)
    if not plan:
        return {"error": "Plan not found"}

    total_fee = calculate_fee(plan["price"], plan["duration"])

    membership = {
        "membership_id": membership_counter,
        "member_name": req.member_name,
        "plan_id": plan["id"],
        "plan_name": plan["name"],
        "duration": plan["duration"],
        "total_fee": total_fee,
        "status": "active"
    }

    memberships.append(membership)
    membership_counter += 1
    return membership

# -----------------------
# PLANS FILTER (Q10)
# -----------------------
@app.get("/plans/filter")
def filter_plans(max_price: int = None):
    if max_price:
        return [p for p in plans if p["price"] <= max_price]
    return plans

# -----------------------
# CREATE PLAN (Q11)
# -----------------------
@app.post("/plans")
def create_plan(plan: NewPlan, response: Response):
    if any(p["name"].lower() == plan.name.lower() for p in plans):
        return {"error": "Duplicate plan"}

    new_plan = {
        "id": len(plans) + 1,
        "name": plan.name,
        "duration": plan.duration_months,
        "price": plan.price,
        "includes_classes": plan.includes_classes,
        "includes_trainer": plan.includes_trainer
    }

    plans.append(new_plan)
    response.status_code = 201
    return new_plan

# -----------------------
# UPDATE PLAN (Q12)
# -----------------------
@app.put("/plans/{plan_id}")
def update_plan(plan_id: int, price: Optional[int] = None):
    plan = find_plan(plan_id)
    if not plan:
        return {"error": "Plan not found"}

    if price:
        plan["price"] = price
    return plan

# -----------------------
# DELETE PLAN (Q13)
# -----------------------
@app.delete("/plans/{plan_id}")
def delete_plan(plan_id: int):
    plan = find_plan(plan_id)
    if not plan:
        return {"error": "Plan not found"}

    if any(m["plan_id"] == plan_id and m["status"] == "active" for m in memberships):
        return {"error": "Cannot delete plan with active memberships"}

    plans.remove(plan)
    return {"message": "Plan deleted"}

# -----------------------
# CLASS BOOKING (Q14)
# -----------------------
@app.post("/classes/book")
def book_class(req: ClassBooking):
    global booking_counter

    membership = next((m for m in memberships if m["member_name"] == req.member_name and m["status"] == "active"), None)
    if not membership:
        return {"error": "No active membership"}

    plan = find_plan(membership["plan_id"])
    if not plan["includes_classes"]:
        return {"error": "Plan does not include classes"}

    booking = {
        "booking_id": booking_counter,
        "member_name": req.member_name,
        "class_name": req.class_name,
        "class_date": req.class_date
    }

    class_bookings.append(booking)
    booking_counter += 1
    return booking

@app.get("/classes/bookings")
def get_bookings():
    return class_bookings

# -----------------------
# Q15
# -----------------------
@app.delete("/classes/cancel/{booking_id}")
def cancel_booking(booking_id: int):
    booking = next((b for b in class_bookings if b["booking_id"] == booking_id), None)
    if not booking:
        return {"error": "Booking not found"}

    class_bookings.remove(booking)
    return {"message": "Booking cancelled"}

@app.put("/memberships/{membership_id}/freeze")
def freeze_membership(membership_id: int):
    m = next((x for x in memberships if x["membership_id"] == membership_id), None)
    if not m:
        return {"error": "Membership not found"}
    m["status"] = "frozen"
    return m

@app.put("/memberships/{membership_id}/reactivate")
def reactivate_membership(membership_id: int):
    m = next((x for x in memberships if x["membership_id"] == membership_id), None)
    if not m:
        return {"error": "Membership not found"}
    m["status"] = "active"
    return m

# -----------------------
# Q16 SEARCH
# -----------------------
@app.get("/plans/search")
def search_plans(keyword: str):
    k = keyword.lower()
    if k == "classes":
        result = [p for p in plans if p["includes_classes"]]
    elif k == "trainer":
        result = [p for p in plans if p["includes_trainer"]]
    else:
        result = [p for p in plans if k in p["name"].lower()]

    return {"total_found": len(result), "plans": result}

# -----------------------
# Q17 SORT
# -----------------------
@app.get("/plans/sort")
def sort_plans(sort_by: str = "price"):
    if sort_by not in ["price", "name", "duration"]:
        return {"error": "Invalid field"}
    return sorted(plans, key=lambda x: x[sort_by])

# -----------------------
# Q18 PAGE
# -----------------------
@app.get("/plans/page")
def page_plans(page: int = 1, limit: int = 2):
    total = len(plans)
    total_pages = math.ceil(total / limit)
    start = (page - 1) * limit
    return {"page": page, "total_pages": total_pages, "data": plans[start:start+limit]}

# -----------------------
# Q19 MEMBERSHIP OPS
# -----------------------
@app.get("/memberships/search")
def search_memberships(name: str):
    return [m for m in memberships if name.lower() in m["member_name"].lower()]

@app.get("/memberships/sort")
def sort_memberships(sort_by: str = "total_fee"):
    return sorted(memberships, key=lambda x: x[sort_by])

@app.get("/memberships/page")
def page_memberships(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return memberships[start:start+limit]

# -----------------------
# Q20 BROWSE
# -----------------------
@app.get("/plans/browse")
def browse(keyword: str = None, includes_classes: bool = None, sort_by: str = "price", page: int = 1, limit: int = 2):
    data = plans

    if keyword:
        data = [p for p in data if keyword.lower() in p["name"].lower()]

    if includes_classes is not None:
        data = [p for p in data if p["includes_classes"] == includes_classes]

    data = sorted(data, key=lambda x: x[sort_by])

    total_pages = math.ceil(len(data)/limit)
    start = (page-1)*limit

    return {"total_pages": total_pages, "data": data[start:start+limit]}