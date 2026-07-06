import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

PRIORITY_COLORS = {"high": "🔴", "medium": "🟡", "low": "🟢"}

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes_per_day=90)

owner = st.session_state.owner
scheduler = Scheduler(owner)

with st.expander("Owner settings", expanded=True):
    owner.name = st.text_input("Owner name", value=owner.name)
    owner.available_minutes_per_day = st.number_input(
        "Available minutes per day", min_value=10, max_value=600,
        value=owner.available_minutes_per_day, step=10
    )

st.divider()
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if owner.get_pet(new_pet_name) is None:
        owner.add_pet(Pet(name=new_pet_name, species=new_pet_species))
        st.success(f"Added {new_pet_name} ({new_pet_species})")
    else:
        st.warning(f"{new_pet_name} already exists")

if not owner.pets:
    st.info("No pets yet. Add one above.")
else:
    st.divider()
    st.subheader("Add a Task")

    pet_names = [p.name for p in owner.pets]
    selected_pet = st.selectbox("Pet", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_date = st.date_input("Date", value=datetime.now())
    with col2:
        task_time = st.time_input("Time", value=datetime.now().replace(second=0, microsecond=0))
    with col3:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        pet = owner.get_pet(selected_pet)
        pet.add_task(Task(
            description=task_title,
            time=task_time.strftime("%H:%M"),
            date=task_date.strftime("%Y-%m-%d"),
            duration_minutes=int(duration),
            priority=priority,
            frequency=frequency,
        ))
        st.success(f"Added '{task_title}' for {selected_pet}")

    st.divider()
    st.subheader("All Tasks")
    all_tasks = scheduler.sort_by_time()
    if all_tasks:
        table_rows = [
            {
                "Pet": t.pet_name,
                "Task": t.description,
                "Date": t.date,
                "Time": t.time,
                "Duration": f"{t.duration_minutes} min",
                "Priority": f"{PRIORITY_COLORS.get(t.priority, '')} {t.priority}",
                "Status": "✅ done" if t.completed else "⏳ pending",
            }
            for t in all_tasks
        ]
        st.table(table_rows)
    else:
        st.info("No tasks yet. Add one above.")

    st.divider()
    st.subheader("Conflicts")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for task_a, task_b in conflicts:
            st.warning(
                f"⚠️ '{task_a.description}' ({task_a.pet_name}) and "
                f"'{task_b.description}' ({task_b.pet_name}) are both scheduled "
                f"at {task_a.time} on {task_a.date}"
            )
    else:
        st.success("✅ No conflicts found")

    st.divider()
    st.subheader("Build Daily Plan")
    plan_date = st.date_input("Plan for date", value=datetime.now(), key="plan_date")

    if st.button("Generate schedule"):
        plan = scheduler.build_daily_plan(date=plan_date.strftime("%Y-%m-%d"))
        if not plan:
            st.info("No tasks scheduled for this date.")
        else:
            for entry in plan:
                task = entry["task"]
                label = f"{PRIORITY_COLORS.get(task.priority, '')} **{task.time}** — {task.description} ({task.pet_name})"
                if entry["included"]:
                    st.success(f"{label}\n\n{entry['reason']}")
                else:
                    st.warning(f"{label}\n\n{entry['reason']}")

    st.divider()
    st.subheader("Save / Load")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save to data.json"):
            scheduler.save_to_json("data.json")
            st.success("Saved to data.json")
    with col2:
        if st.button("Load from data.json"):
            try:
                st.session_state.owner = scheduler.load_from_json("data.json")
                st.success("Loaded from data.json")
            except FileNotFoundError:
                st.error("No data.json found yet — save first.")