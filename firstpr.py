import streamlit as st
import pymysql
import pandas as pd

# ------------------ Database Connection ------------------
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='admin@123',
    database='food_wastage_solutn')

# ------------------ Page Config ------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #94A835 !important;
    font-family: 'Poppins', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #6D7B66 !important;
}
.info-card {
    background-color: #fff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}
h1, h2, h3 {
    color: #2E3B1F;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------ Sidebar Navigation ------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Introduction", "View Tables", "Search", "CRUD Operation", "Personal Details", "SQL Query & Visualization","extra SQL Query", "user intro"])

# ------------------ Page: Introduction ------------------
if page == "Introduction":
    st.markdown("""
    <h1 style="text-align: center; font-weight: bold; color: #252121;">
        Food Wastage Management System
    </h1>
""", unsafe_allow_html=True)
    st.markdown("""
    ### 🌱 Why This Matters
    Food wastage is a significant issue, with many households and restaurants discarding surplus food while numerous people struggle with food insecurity.

    This system bridges the gap between **food providers** and **receivers**, enabling:
    - 🍽️ Restaurants and individuals can list surplus food.
    - 🏥 NGOs or individuals in need can claim the food.
    - 🔗 Connecting surplus food providers to those in need through a structured platform.
    - ♻️ **Reducing food waste** by redistributing excess food efficiently.
    - 📊 Data analysis on food wastage trends for better decision-making.
    """)

# ------------------ Page: View Tables ------------------
elif page == "View Tables":
    st.header("📋 View Tables")
    tables = ["providers_data", "receivers_data", "food_listings_data", "claims_data"]
    selected_table = st.selectbox("Select a table to view", tables)

    query = f"SELECT * FROM {selected_table} LIMIT 1000"
    df = pd.read_sql(query, connection)
    st.dataframe(df)

    # ------------------ Page: Search ------------------
elif page == "Search":

    st.header("🔍 Search Records")
    table_choice = st.selectbox("Select a table to search",["food_listings_data", "providers_data", "receivers_data", "claims_data"])
    
    if table_choice == "food_listings_data":
        st.subheader("Search Food Listings")
        search_by = st.selectbox("Search by", ["Food_ID", "Food_Name", "Provider_Type", "Location", "Food_Type"])
        if search_by == "Food_ID":
            food_id = st.text_input("Enter Food_ID")
            if st.button("Proceed"):
                query = f"SELECT * FROM food_listings_data WHERE Food_ID = '{food_id}'"
                df = pd.read_sql(query, connection)
                st.dataframe(df if not df.empty else pd.DataFrame(["Enter a valid Food_ID"], columns=["Message"]))
        else:
                options = pd.read_sql(f"SELECT DISTINCT {search_by} FROM food_listings_data", connection)[search_by].dropna().tolist()
                selected = st.selectbox(f"Choose {search_by}", options)
                query = f"SELECT * FROM food_listings_data WHERE {search_by} = '{selected}'"
                df = pd.read_sql(query, connection)
                st.dataframe(df)

    elif table_choice == "providers_data":
        st.subheader("Search Providers")
        search_by = st.selectbox("Search by", ["Provider_ID", "Type"])
        if search_by == "Provider_ID":
            pid = st.text_input("Enter Provider_ID")
            if st.button("Proceed"):
                query = f"SELECT * FROM providers_data WHERE Provider_ID = '{pid}'"
                df = pd.read_sql(query, connection)
                st.dataframe(df if not df.empty else pd.DataFrame(["Enter a valid Provider_ID"], columns=["Message"]))
        else:
                types = pd.read_sql("SELECT DISTINCT Type FROM providers_data", connection)["Type"].dropna().tolist()
                selected = st.multiselect("Choose Provider Type", types)
                if selected:
                    placeholders = ', '.join([f"'{t}'" for t in selected])
                    query = f"SELECT * FROM providers_data WHERE Type IN ({placeholders})"
                    df = pd.read_sql(query, connection)
                    st.dataframe(df)
                
    elif table_choice == "receivers_data":
            st.subheader("Search Receivers")
            search_by = st.selectbox("Search by", ["Receiver_ID", "Type"])
            if search_by == "Receiver_ID":
                rid = st.text_input("Enter Receiver_ID")
                if st.button("Proceed"):
                    query = f"SELECT * FROM receivers_data WHERE Receiver_ID = '{rid}'"
                    df = pd.read_sql(query, connection)
                    st.dataframe(df if not df.empty else pd.DataFrame(["Enter a valid Receiver_ID"], columns=["Message"]))
            else:
                types = pd.read_sql("SELECT DISTINCT Type FROM receivers_data", connection)["Type"].dropna().tolist()
                selected = st.multiselect("Choose Receiver Type", types)
                if selected:
                    placeholders = ', '.join([f"'{t}'" for t in selected])
                    query = f"SELECT * FROM receivers_data WHERE Type IN ({placeholders})"
                    df = pd.read_sql(query, connection)
                    st.dataframe(df)
                    
    elif table_choice == "claims_data":
        st.subheader("Search Claims")
        search_by = st.selectbox("Search by", ["Claim_ID", "Status", "Timestamp"])
        if search_by == "Claim_ID":
            cid = st.text_input("Enter Claim_ID")
            if st.button("Proceed"):
                query = f"SELECT * FROM claims_data WHERE Claim_ID = '{cid}'"
                df = pd.read_sql(query, connection)
                st.dataframe(df if not df.empty else pd.DataFrame(["Enter a valid Claim_ID"], columns=["Message"]))
        elif search_by == "Status":
            status = st.radio("Choose claims Status", ["Pending", "Cancelled", "Completed"])
            query = f"SELECT * FROM claims_data WHERE Status = '{status}'"
            df = pd.read_sql(query, connection)
            st.dataframe(df)

            # ------------------ Page: CRUD Operation ------------------
elif page == "CRUD Operation":
    st.header("🛠️ CRUD Operations")

    crud_action = st.selectbox("Choose Operation", ["Create", "Read", "Update", "Delete"])
    table_choice = st.selectbox("Select Table", ["food_listings_data", "providers_data", "receivers_data", "claims_data"])
    
    cursor = connection.cursor()

    # ---------- FOOD LISTINGS ----------
    if table_choice == "food_listings_data":
        if crud_action == "Create":
            st.subheader("Add New Food Listing")
            Food_ID = st.number_input("Food_ID")
            Food_Name = st.text_input("Food_Name")
            Quantity = st.number_input("Quantity")
            Expiry_Date = st.text_input("Expiry_Date")
            Provider_ID = st.number_input("Provider_ID")
            Provider_Type = st.text_input("Provider_Type")
            Location = st.text_input("Location")
            Food_Type = st.text_input("Food_Type")
            Meal_Type = st.text_input("Meal_Type")
            if st.button("Add"):
                if all([Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type]):
                    cursor.execute(
                    "INSERT INTO food_listings_data (Food_ID,Food_Name,Quantity,Expiry_Date,Provider_ID,Provider_Type,Location,Food_Type,Meal_Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                    )
                    connection.commit()
                    st.success("Food listing added!")
                else:
                    st.warning("Please fill in all fields before submitting.")

        elif crud_action == "Read":
            st.subheader("View Food Listings")
            df = pd.read_sql("SELECT * FROM food_listings_data", connection)
            st.dataframe(df)

        elif crud_action == "Update":
            st.subheader("Update Food Listing")
            fid = st.text_input("Enter Food_ID to update")
            if fid:
                df = pd.read_sql(f"SELECT * FROM food_listings_data WHERE Food_ID = '{fid}'", connection)
                if not df.empty:
                    Food_Name = st.text_input("Food_Name", df["Food_Name"][0])
                    Quantity = st.number_input("Quantity", df["Quantity"][0])
                    Expiry_Date = st.text_input("Expiry_Date", df["Expiry_Date"][0])
                    Provider_ID = st.number_input("Provider_ID", df["Provider_ID"][0])
                    Provider_Type = st.text_input("Provider_Type", df["Provider_Type"][0])
                    Location = st.text_input("Location", df["Location"][0])
                    Food_Type = st.text_input("Food_Type", df["Food_Type"][0])
                    Meal_Type = st.text_input("Meal_Type", df["Meal_Type"][0])
                    if st.button("Update"):
                        cursor.execute("""
                            UPDATE food_listings_data 
                            SET Food_Name=%s, Quantity=%s, Expiry_Date=%s, Provider_ID=%s, Provider_Type=%s, Location=%s, Food_Type=%s, Meal_Type=%s 
                            WHERE Food_ID=%s""", (Food_Name, Quantity, Expiry_Date, Provider_ID,Provider_Type,Location,Food_Type,Meal_Type, fid))
                        connection.commit()
                        st.success("Food listing updated!")
                else:
                    st.error("Food_ID not found")

        elif crud_action == "Delete":
            st.subheader("Delete Food Listing")
            fid = st.text_input("Enter Food_ID to delete")
            if st.button("Delete"):
                cursor.execute("DELETE FROM food_listings_data WHERE Food_ID = %s", (fid,))
                connection.commit()
                st.success("Food listing deleted!")

    # ---------- PROVIDERS ----------
    elif table_choice == "providers_data":
        if crud_action == "Create":
            st.subheader("Add New Provider")
            pid = st.number_input("Provider_ID")
            Name = st.text_input("Name")
            Type = st.text_input("Type")
            Address = st.text_input("Address")
            City = st.text_input("City")
            Contact = st.text_input("Contact")
            if st.button("Add"):
                cursor.execute("INSERT INTO providers_data VALUES (%s, %s, %s, %s, %s, %s)", (pid, Name,Type,Address,City,Contact))
                connection.commit()
                st.success("Provider added!")

        elif crud_action == "Read":
            st.subheader("View Providers")
            df = pd.read_sql("SELECT * FROM providers_data", connection)
            st.dataframe(df)

        elif crud_action == "Update":
            st.subheader("Update Provider")
            pid = st.text_input("Enter Provider_ID to update")
            if pid:
                df = pd.read_sql(f"SELECT * FROM providers_data WHERE Provider_ID = '{pid}'", connection)
                if not df.empty:
                    Name = st.text_input("Name",df["Name"][0])
                    Type = st.text_input("Type", df["Type"][0])
                    Address = st.text_input("Address", df["Address"][0])
                    City = st.text_input("City", df["City"][0])
                    Contact = st.text_input("Contact", df["Contact"][0])
                    if st.button("Update"):
                        cursor.execute("UPDATE providers_data SET Name=%s, Type=%s, Address=%s,City=%s,Contact=%s WHERE Provider_ID=%s", (Name,Type,Address,City,Contact, pid))
                        connection.commit()
                        st.success("Provider updated!")
                else:
                    st.error("Provider_ID not found")

        elif crud_action == "Delete":
            st.subheader("Delete Provider")
            pid = st.text_input("Enter Provider_ID to delete")
            if st.button("Delete"):
                cursor.execute("DELETE FROM providers_data WHERE Provider_ID = %s", (pid,))
                connection.commit()
                st.success("Provider deleted!")

    # ---------- RECEIVERS ----------
    elif table_choice == "receivers_data":
        if crud_action == "Create":
            st.subheader("Add New Receiver")
            rid = st.number_input("Receiver_ID")
            Name = st.text_input("Name")
            Type = st.text_input("Type")
            City = st.text_input("City")
            Contact = st.text_input("Contact")
            if st.button("Add"):
                cursor.execute("INSERT INTO receivers_data VALUES (%s, %s, %s, %s, %s)", (rid, Name,Type,City,Contact))
                connection.commit()
                st.success("Receiver added!")

        elif crud_action == "Read":
            st.subheader("View Receivers")
            df = pd.read_sql("SELECT * FROM receivers_data", connection)
            st.dataframe(df)

        elif crud_action == "Update":
            st.subheader("Update Receiver")
            rid = st.text_input("Enter Receiver_ID to update")
            if rid:
                df = pd.read_sql(f"SELECT * FROM receivers_data WHERE Receiver_ID = '{rid}'", connection)
                if not df.empty:
                    Name = st.text_input("Name",df["Name"][0])
                    Type = st.text_input("Type",df["Type"][0])
                    City = st.text_input("City",df["City"][0])
                    Contact = st.text_input("Contact",df["Contact"][0])
                    if st.button("Update"):
                        cursor.execute("UPDATE receivers_data SET Name=%s, Type=%s, City=%s,Contact=%s WHERE Receiver_ID=%s", (Name,Type,City,Contact, rid))
                        connection.commit()
                        st.success("Receiver updated!")
                else:
                    st.error("Receiver_ID not found")

        elif crud_action == "Delete":
            st.subheader("Delete Receiver")
            rid = st.text_input("Enter Receiver_ID to delete")
            if st.button("Delete"):
                cursor.execute("DELETE FROM receivers_data WHERE Receiver_ID = %s", (rid,))
                connection.commit()
                st.success("Receiver deleted!")

    # ---------- CLAIMS ----------
    elif table_choice == "claims_data":
        if crud_action == "Create":
            st.subheader("Add New Claim")
            cid = st.number_input("Claim_ID")
            Food_ID = st.number_input("Food_ID")
            Receiver_ID = st.number_input("Receiver_ID")
            status = st.text_input("Status")
            timestamp = st.text_input("Timestamp")
            if st.button("Add"):
                cursor.execute("INSERT INTO claims_data VALUES (%s, %s, %s, %s, %s)", (cid,Food_ID,Receiver_ID, status, timestamp))
                connection.commit()
                st.success("Claim added!")

        elif crud_action == "Read":
            st.subheader("View Claims")
            df = pd.read_sql("SELECT * FROM claims_data", connection)
            st.dataframe(df)

        elif crud_action == "Update":
            st.subheader("Update Claim")
            cid = st.text_input("Enter Claim_ID to update")
            if cid:
                df = pd.read_sql(f"SELECT * FROM claims_data WHERE Claim_ID = '{cid}'", connection)
                if not df.empty:
                    Food_ID = st.number_input("Food_ID",df["Food_ID"][0])
                    Receiver_ID = st.number_input("Receiver_ID",df["Receiver_ID"][0])
                    status = st.text_input("Status",df["status"][0])
                    timestamp = st.text_input("Timestamp",df["timestamp"][0])
                    if st.button("Update"):
                        cursor.execute("UPDATE claims_data SET Food_ID=%s,Receiver_ID=%s, Status=%s, Timestamp=%s WHERE Claim_ID=%s", 
                                       (Food_ID,Receiver_ID,status, timestamp, cid))
                        connection.commit()
                        st.success("Claim updated!")
                else:
                    st.error("Claim_ID not found")

        elif crud_action == "Delete":
            st.subheader("Delete Claim")
            cid = st.text_input("Enter Claim_ID to delete")
            if st.button("Delete"):
                cursor.execute("DELETE FROM claims_data WHERE Claim_ID = %s", (cid,))
                connection.commit()
                st.success("Claim deleted!")

              # ------------------ Page: SQL Query & Visualization ------------------
elif page == "SQL Query & Visualization":
    st.header("📊 SQL Query & Visualization")

    query_options = [
        "1. Providers and Receivers Count by City",
        "2. Provider Type with Most Food Contributions",
        "3. Contact Info of Providers in a Specific City",
        "4. Receivers Who Claimed the Most Food",
        "5. Total Quantity of Food Available",
        "6. City with the Highest Number of Food Listings",
        "7. Most Commonly Available Food Types",
        "8. Food Claims Count for Each Food Item",
        "9. Provider with Highest Number of Successful Claims",
        "10. Claim Status Percentage (Completed vs. Pending vs. Canceled)",
        "11. Average Quantity of Food Claimed Per Receiver",
        "12. Most Claimed Meal Type",
        "13. Total Quantity of Food Donated by Each Provider"
    ]

    selected_query = st.selectbox("Select a SQL Analysis", query_options)
    cursor = connection.cursor()

    # Define SQL queries
    queries = {
        query_options[0]: """SELECT 
                l.Location,
                COUNT(p.Provider_ID) AS Provider_count,
                COUNT(r.Receiver_ID) AS Receiver_count
            FROM food_wastage_solutn.food_listings_data l
            LEFT JOIN providers_data p ON p.Provider_ID = l.Provider_ID
            LEFT JOIN claims_data c ON c.Food_ID = l.Food_ID
            LEFT JOIN receivers_data r ON r.Receiver_ID = c.Receiver_ID
            GROUP BY l.Location""",

        query_options[1]: """SELECT p.Type, COUNT(p.Provider_ID) AS Provider_count FROM providers_data p GROUP BY p.Type
                                ORDER BY Provider_count DESC ;""",

        query_options[2]: """SELECT l.Location, p.Provider_ID, p.Name, p.Contact, p.Address, p.city FROM providers_data p
                             JOIN food_listings_data l ON l.Provider_ID = p.Provider_ID
                             WHERE l.Location = 'South Kellyville' order by l.Location;""", 

        query_options[3]: """SELECT Receiver_ID, Name, claim_count
                                FROM (
                                    SELECT r.Receiver_ID, r.Name, COUNT(c.Claim_ID) AS claim_count,
                                    RANK() OVER (ORDER BY COUNT(c.Claim_ID) DESC) AS rank_val
                                    FROM receivers_data r
                                    JOIN claims_data c ON c.Receiver_ID = r.Receiver_ID
                                    GROUP BY r.Receiver_ID, r.Name
                                ) AS ranked
                                WHERE rank_val = 1
                                ORDER BY Receiver_ID;""",

        query_options[4]: """select sum(l.Quantity) as total_food_qty from food_listings_data l
                                join providers_data p on p.Provider_ID=l.Provider_ID order by total_food_qty""",

        query_options[5]: """SELECT Location, foodlist_count
                             FROM (
                                SELECT Location,COUNT(*) AS foodlist_count,RANK() OVER (ORDER BY COUNT(*) DESC) AS rank_val
                                FROM food_listings_data
                                GROUP BY Location) AS ranked_locations
                            WHERE rank_val = 1
                            ORDER BY Location;""",

        query_options[6]: """select Food_Type,COUNT(*) AS listing_count FROM food_listings_data
                             GROUP BY Food_Type ORDER BY listing_count DESC;""",

        query_options[7]: """SELECT l.Food_Name, COUNT(c.Claim_ID) AS total_claims FROM food_listings_data l
                             left join claims_data c on c.Food_ID= l.Food_ID
                             GROUP BY  l.Food_Name ORDER BY total_claims DESC;""",

        query_options[8]: """SELECT p.Name,count(c.Claim_ID) as claim_count FROM providers_data p 
                             inner join food_listings_data l on l.Provider_ID = p.Provider_ID
                             inner join claims_data c on c.Food_ID= l.Food_ID where c.Status = 'Completed' GROUP BY  p.Provider_ID,p.Name
                             order by claim_count desc Limit 5;
                             """,

        query_options[9]: """SELECT Status as Claim_Status,ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims_data)), 2) AS percentage
                                FROM claims_data GROUP BY Status;""",

        query_options[10]: """SELECT r.Receiver_ID,r.Name,ROUND(AVG(l.Quantity), 2) AS avg_quantity_claimed from food_wastage_solutn.receivers_data r
                                join claims_data c on c.Receiver_ID=r.Receiver_ID 
                                join food_listings_data l on l.Food_ID=c.Food_ID
                                group by r.Receiver_ID,r.Name order by avg_quantity_claimed desc""",

        query_options[11]: """SELECT l.Meal_Type,count(c.Claim_ID) as claim_count FROM food_listings_data l 
                                inner join claims_data c on c.Food_ID= l.Food_ID
                                GROUP BY  l.Meal_Type order by claim_count desc """,

        query_options[12]: """SELECT p.Provider_ID,p.Name,sum(l.Quantity) as food_qty FROM providers_data p
                                inner join food_listings_data l on l.Provider_ID = p.Provider_ID
                                GROUP BY  p.Provider_ID,p.Name order by food_qty desc"""
    }

    # Run selected query
    if selected_query in queries:
        df = pd.read_sql(queries[selected_query], connection)
        st.dataframe(df)

        # Map query to visualization type
        visualization_map = {
            query_options[1]: "bar",   
            query_options[6]: "dot",    # food type
            query_options[7]: "bar", 
            query_options[8]: "bar", 
            query_options[9]: "pie",       # e.g., Claim Status
            query_options[11]: "bar"   
                            }
        if selected_query in visualization_map:
            st.subheader("📈 Visualization")
            import matplotlib.pyplot as plt
            import seaborn as sns

            plt.figure(figsize=(6, 3))
            chart_type = visualization_map[selected_query]

            if chart_type == "pie":
                plt.pie(df['percentage'], labels=df['Claim_Status'], autopct='%1.1f%%', radius=0.7)
                plt.title("Claim Status Distribution")

            elif chart_type == "dot":
                x_col = df.columns[0]
                y_col = df.columns[1]
                sns.stripplot(x=x_col, y=y_col, data=df, size=4, jitter=True)
                plt.xticks(rotation=45)
                plt.title(f"{x_col} vs {y_col}")

            elif chart_type == "bar":
                x_col = df.columns[0]
                y_col = df.columns[1]
                sns.barplot(x=x_col, y=y_col, data=df, width=0.4)
                plt.xticks(rotation=45)
                plt.title(f"{x_col} vs {y_col}")

            st.pyplot(plt)

      # ------------------ extra SQL Query  -----------------
elif page == "extra SQL Query":
    st.header("✏️ extra SQL Query")

    query_options = ["1. Which food items are most frequently claimed before their expiry date?","2. Which cities have the highest ratio of claims to listings?","3.  What is the distribution of food types claimed by receiver type?","4. What is the distribution percentages of food types claimed by each receiver type?","5. which receiver type have highest receivers?",
                     "6. Which city have heighest number of food claims", "7. location wise number of food list and claims made"  
                     ]

    selected_query = st.selectbox("Select a SQL Analysis", query_options)
    cursor = connection.cursor()

    # Define SQL queries
    queries = {
                query_options[0]: """SELECT fl.Food_Name,COUNT(c.Claim_ID) AS Claims_Before_Expiry FROM claims_data c
                             JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID WHERE c.Timestamp < fl.Expiry_Date
                             GROUP BY fl.Food_Name ORDER BY Claims_Before_Expiry DESC LIMIT 10;""",

                query_options[1]: """SELECT fl.location,COUNT(DISTINCT c.Claim_ID) AS Total_Claims,COUNT(DISTINCT fl.Food_ID) AS Total_Listings,
                             ROUND(COUNT(DISTINCT c.Claim_ID) / COUNT(DISTINCT fl.Food_ID), 2) AS Claim_to_Listing_Ratio FROM food_listings_data fl
                             LEFT JOIN claims_data c ON fl.Food_ID = c.Food_ID GROUP BY fl.Location HAVING Total_Listings > 0
                             ORDER BY Claim_to_Listing_Ratio DESC;""",

                query_options[2]: """ SELECT r.type as Receiver_Type,fl.Food_Type,COUNT(*) AS Total_Claims FROM claims_data c
                             JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
                             JOIN receivers_data r ON c.Receiver_ID = r.Receiver_ID GROUP BY r.type, fl.Food_Type ORDER BY r.type, Total_Claims DESC;""",

                query_options[3]: """SELECT r.Type as Receiver_Type,fl.Food_Type,COUNT(*) AS Total_Claims,ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY r.Type), 2) AS Percentage_Within_Receiver
                             FROM claims_data c
                             JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
                             JOIN receivers_data r ON c.Receiver_ID = r.Receiver_ID
                             GROUP BY r.Type, fl.Food_Type ORDER BY r.Type, Percentage_Within_Receiver DESC;""",

                query_options[4]: """SELECT r.Type, COUNT(r.Receiver_ID) AS Receiver_count FROM receivers_data r GROUP BY r.Type ORDER BY Receiver_count DESC LIMIT 1;""",

                query_options[5]: """ SELECT city, claim_count FROM ( SELECT r.city, COUNT(c.Claim_ID) AS claim_count, RANK() OVER (ORDER BY COUNT(c.Claim_ID) DESC) AS rk FROM receivers_data r INNER JOIN claims_data c ON c.Receiver_ID = r.Receiver_ID GROUP BY r.city) AS ranked WHERE rk = 1;""",

                query_options[6]: """ select l.location, count(l.Food_ID) as food_listing_count, count(c.Claim_ID) claim_count FROM food_listings_data l left join claims_data c on c.Food_ID= l.Food_ID GROUP BY l.Location order by food_listing_count desc """
    }
        # Run selected query
    if selected_query in queries:
        df = pd.read_sql(queries[selected_query], connection)
        st.dataframe(df)

        # ------------------ Page: Personal Details ------------------

elif page == "Personal Details":
    st.header("👤 Personal Details Lookup")
    st.markdown("Easily check details of a provider or receiver by entering their ID.")

    choice = st.selectbox("Select Type", ["Provider", "Receiver"])
    entered_id = st.text_input(f"Enter {choice}_ID")

    if st.button("Get Details"):
        if choice == "Provider":
            query = f"SELECT * FROM providers_data WHERE Provider_ID = '{entered_id}'"
        else:
            query = f"SELECT * FROM receivers_data WHERE Receiver_ID = '{entered_id}'"

        df = pd.read_sql(query, connection)
        if not df.empty:
            st.success("✅ Valid ID Found!")
            st.markdown("<div class='info-card'>", unsafe_allow_html=True)
            st.write(df)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ Invalid ID. Please check again.")

            # ------------------ Page: user intro ------------------
elif page == "user intro":
    st.markdown("""
    <h1 style="text-align:center;">👋 About Me</h1>
    """, unsafe_allow_html=True)
    st.markdown("""
    ### Hi, I'm **Niketa Singh** 💫  
    the creator and developer of this Food Wastage Management System. 
            I'm a beginner enthusiast in database management and application development. 
            This mini-project represents my dedication to learning **MySQL, Python and Streamlit** 
            with the goal of building practical solutions to real-world problems like food waste. 🌱**
    """)
    st.markdown("---")
    st.caption("Made with ❤️ ")
