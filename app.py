#Import required packages
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# FUNCTION TO CONNECT DATABASE
# ---------------------------------------------------------

def get_data(query, params=None):

    conn = sqlite3.connect("traffic_crash.sqlite")

    if params:
        df = pd.read_sql_query(query, conn, params=params)

    else:
        df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# ---------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Traffic Crash Analytics & Safety Intelligence Platform",
    layout="wide"
)

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Project Introduction",
        "Traffic Crash Data Visualization",
        "SQL Queries",
        "Creator Info"
    ]
)

# =========================================================
# PAGE 1 : PROJECT INTRODUCTION
# =========================================================

if page == "Project Introduction":

    st.title("🚗 Traffic Crash Analysis")
    
    # Image
    # Make sure image exists in project folder
    st.image(
        "traffic_crash.jpg",
        width="stretch"
    )

    st.subheader(
        "📊 A Streamlit App for Analysing Traffic Crashes"
    )

    st.write("""
    This project analyzes traffic crash data using an SQLite database.

    It provides insights into crash frequency, injuries,
    hotspot zones, weather impact, and traffic conditions
    through interactive visualizations and SQL analysis.

    **Features:**

    - View and analyze crash trends by year, month, day, and hour.
    - Identify high-risk locations and hotspot zones.
    - Explore injury patterns based on weather and lighting conditions.
    - Run advanced SQL queries using CTEs and window functions to explore insights.
             
    **Database Used:** `traffic_crash.sqlite`
    """)

# =========================================================
# PAGE 2 : DATA VISUALIZATION
# =========================================================

elif page == "Traffic Crash Data Visualization":

    st.title("🚗 Traffic Crash Data Visualizer")

    # ---------------------------------------------------------
    # FETCH STREET NAMES
    # ---------------------------------------------------------

    streets = get_data(
        """
        SELECT DISTINCT STREET_NAME
        FROM crash_data
        WHERE STREET_NAME IS NOT NULL
        """
    )["STREET_NAME"].tolist()

    # ---------------------------------------------------------
    # STREET DROPDOWN
    # ---------------------------------------------------------

    selected_street = st.selectbox(
        "Select Street",
        streets
    )

    # ---------------------------------------------------------
    # FILTER OPTIONS
    # ---------------------------------------------------------

    filter_option = st.radio(
        "Filter By:",
        [
            "Crash Year",
            "Crash Month",
            "Weather Condition"
        ]
    )

    # =========================================================
    # YEAR FILTER
    # =========================================================

    if filter_option == "Crash Year":

        selected_year = st.selectbox(
            "Select Year",

            sorted(
                get_data(
                    """
                    SELECT DISTINCT year
                    FROM crash_data
                    ORDER BY year
                    """
                )["year"].tolist()
            )
        )

        query = """
        SELECT *
        FROM crash_data
        WHERE STREET_NAME = ?
          AND year = ?
        """

        df = get_data(
            query,
            params=(selected_street, selected_year)
        )

    # =========================================================
    # MONTH FILTER
    # =========================================================

    elif filter_option == "Crash Month":

        selected_month = st.selectbox(
            "Select Month",
            range(1, 13)
        )

        query = """
        SELECT *
        FROM crash_data
        WHERE STREET_NAME = ?
          AND CRASH_MONTH = ?
        """

        df = get_data(
            query,
            params=(selected_street, selected_month)
        )

    # =========================================================
    # WEATHER FILTER
    # =========================================================

    else:

        weather_conditions = get_data(
            """
            SELECT DISTINCT WEATHER_CONDITION
            FROM crash_data
            WHERE WEATHER_CONDITION IS NOT NULL
            """
        )["WEATHER_CONDITION"].tolist()

        selected_weather = st.selectbox(
            "Select Weather Condition",
            weather_conditions
        )

        query = """
        SELECT *
        FROM crash_data
        WHERE STREET_NAME = ?
          AND WEATHER_CONDITION = ?
        """

        df = get_data(
            query,
            params=(selected_street, selected_weather)
        )

    # =========================================================
    # DISPLAY DATA
    # =========================================================

    if not df.empty:

        st.write("### Crash Data")

        st.dataframe(df)

        # ---------------------------------------------------------
        # CREATE SUBPLOTS
        # ---------------------------------------------------------

        st.write("## Traffic Crash Analysis Dashboard")

        # Convert date column
        df["CRASH_DATE"] = pd.to_datetime(
            df["CRASH_DATE"]
        )

        # Sort values
        df = df.sort_values("CRASH_DATE")

        # Create subplot figure
        fig, axes = plt.subplots(
            1,
            3,
            figsize=(18, 10)
        )

        # =========================================================
        # 1. LINE CHART
        # =========================================================

        sns.lineplot(
            data=df,
            x="CRASH_DATE",
            y="INJURIES_TOTAL",
            marker="o",
            ax=axes[0]
        )

        axes[0].set_title(
            "Total Injuries Over Time"
        )

        axes[0].set_xlabel(
            "Crash Date"
        )

        axes[0].set_ylabel(
            "Injuries Total"
        )

        axes[0].tick_params(
            axis='x',
            rotation=45
        )

        # =========================================================
        # 2. BAR CHART
        # =========================================================

        weather_injuries = df.groupby(
            "WEATHER_CONDITION"
        )["INJURIES_TOTAL"].sum().reset_index()

        sns.barplot(
            data=weather_injuries,
            x="WEATHER_CONDITION",
            y="INJURIES_TOTAL",
            ax=axes[1]
        )

        axes[1].set_title(
            "Weather Condition vs Total Injuries"
        )

        axes[1].set_xlabel(
            "Weather Condition"
        )

        axes[1].set_ylabel(
            "Total Injuries"
        )

        axes[1].tick_params(
            axis='x',
            rotation=45
        )

        # =========================================================
        # 3. HISTOGRAM
        # =========================================================

        sns.histplot(
            data=df,
            x="INJURIES_TOTAL",
            bins=20,
            ax=axes[2]
        )

        axes[2].set_title(
            "Distribution of Crash Injuries"
        )

        axes[2].set_xlabel(
            "Injuries Total"
        )

        axes[2].set_ylabel(
            "Frequency"
        )

        # ---------------------------------------------------------
        # LAYOUT ADJUSTMENT
        # ---------------------------------------------------------

        plt.tight_layout()

        # ---------------------------------------------------------
        # DISPLAY SUBPLOTS
        # ---------------------------------------------------------

        st.pyplot(fig)

        # ---------------------------------------------------------
        # CRASH TYPE DISTRIBUTION
        # ---------------------------------------------------------

        st.write("### Crash Type Distribution")

        plt.figure(figsize=(10, 5))

        sns.countplot(
            y=df["CRASH_TYPE"],
            palette="coolwarm"
        )

        plt.xlabel("Count")

        plt.ylabel("Crash Type")

        st.pyplot(plt)

    else:

        st.warning(
            "No crash data available for selected filters."
        )

# =========================================================
# PAGE 3 : SQL QUERIES
# =========================================================

elif page == "SQL Queries":

    st.title("📋 Traffic Crash SQL Query Results")

    queries = {

        "1.Top 5 most dangerous combinations of weather and crash type":
        """
        SELECT 
            WEATHER_CONDITION,CRASH_TYPE,
            COUNT(*) AS TOTAL_CRASHES
        FROM crash_data
        GROUP BY WEATHER_CONDITION,CRASH_TYPE
        ORDER BY TOTAL_CRASHES DESC
        LIMIT 5;
        """
    ,
        
        "2. Top 10 streets with the highest number of injury crashes":
        """
        SELECT
          STREET_NAME,
          COUNT(*) AS TOTAL_INJURY_CRASHES
        FROM crash_data
        WHERE
          INJURIES_TOTAL > 0
        GROUP BY
          STREET_NAME
        ORDER BY
          TOTAL_INJURY_CRASHES DESC
        LIMIT 10;
        """
        ,

        "3. Percentage of crashes that resulted in injuries for each crash type ":
        """
        SELECT
        CRASH_TYPE,

        COUNT(*) AS total_crashes,

        SUM(
            CASE
                WHEN INJURIES_TOTAL > 0 THEN 1
                ELSE 0
            END
        ) AS injury_crashes,

        ROUND(
            (
                SUM(
                    CASE
                        WHEN INJURIES_TOTAL > 0 THEN 1
                        ELSE 0
                    END
                ) * 100.0
            ) / COUNT(*),
            2
        ) AS injury_percentage

        FROM crash_data

        GROUP BY CRASH_TYPE

        ORDER BY injury_percentage DESC;
        """
        , 

        "4. Peak crash hour for each month":
    """
    WITH monthly_hourly_crashes AS
    (
        SELECT
            CRASH_MONTH,
            CRASH_HOUR,
            COUNT(*) AS total_crashes,

            RANK() OVER(
                PARTITION BY CRASH_MONTH
                ORDER BY COUNT(*) DESC
            ) AS crash_rank

        FROM crash_data

        GROUP BY
            CRASH_MONTH,
            CRASH_HOUR
    )

    SELECT
        CRASH_MONTH,
        CRASH_HOUR AS peak_crash_hour,
        total_crashes

    FROM monthly_hourly_crashes

    WHERE crash_rank = 1

    ORDER BY CRASH_MONTH;
    """     
        ,

        "5. Top 5 primary causes of crashes during night time (CRASH_HOUR ≥ 18) ": 
        """
        SELECT
           PRIM_CONTRIBUTORY_CAUSE,
           COUNT(*) AS TOTAL_CRASHES
        FROM crash_data
        WHERE
           CRASH_HOUR >= 18
        GROUP BY
           PRIM_CONTRIBUTORY_CAUSE
        ORDER BY
           TOTAL_CRASHES DESC
        LIMIT 5;
        """
        ,

        "6. Average number of injuries in daylight vs darkness conditions": 
        """
        SELECT 
            LIGHTING_CONDITION,
            ROUND(AVG(INJURIES_TOTAL), 2) AS avg_injuries
        FROM crash_data
        WHERE LIGHTING_CONDITION IN 
        (
            'DAYLIGHT',
            'DARKNESS'
        )
        AND INJURIES_TOTAL IS NOT NULL
        GROUP BY LIGHTING_CONDITION;
        """
        ,

        "7. Traffic control device type has the highest average injuries per crash":
        """
        SELECT 
            TRAFFIC_CONTROL_DEVICE,
            ROUND(AVG(INJURIES_TOTAL),2) AS INJURIES
        FROM crash_data
        WHERE 
            TRAFFIC_CONTROL_DEVICE IS NOT NULL 
            AND INJURIES_TOTAL IS NOT NULL
        GROUP BY 
            TRAFFIC_CONTROL_DEVICE
        ORDER BY 
            INJURIES DESC
        LIMIT 1;
        """
        ,

        "8. Top 5 locations (latitude/longitude) with the highest crash frequency":
        """
        SELECT 
            STREET_NAME,
            LOCATION,
            LATITUDE,
            LONGITUDE,
            COUNT(*) AS crash_frequency
        FROM crash_data
        WHERE 
            LATITUDE IS NOT NULL AND 
            LONGITUDE IS NOT NULL
        GROUP BY LOCATION,
            STREET_NAME,
            LATITUDE,
            LONGITUDE
        ORDER BY crash_frequency DESC
        LIMIT 5;
        """
        ,

        "9. Top 5 streets with the highest injury rate and streets with more than 100 crashes":
        """
        WITH street_analysis AS
        (
        SELECT 
            STREET_NAME,
            COUNT(*) AS total_crashes,
            ROUND(AVG(INJURIES_TOTAL), 2) AS injury_rate
        FROM crash_data
        WHERE STREET_NAME IS NOT NULL
        AND INJURIES_TOTAL IS NOT NULL
        GROUP BY STREET_NAME
        )

        SELECT 
            STREET_NAME,
            total_crashes,
            injury_rate
        FROM street_analysis
        WHERE total_crashes > 100
        ORDER BY injury_rate DESC
        LIMIT 5;
        """

        ,

        "10. Identify the most common crash type for each year.":
        """
        WITH yearly_crash_types AS
        (
            SELECT
                year,
                CRASH_TYPE,
                COUNT(*) AS total_crashes,

                RANK() OVER(
                    PARTITION BY year
                    ORDER BY COUNT(*) DESC
                ) AS crash_rank

            FROM crash_data

            GROUP BY
                year,
                CRASH_TYPE
        )

        SELECT
            year,
            CRASH_TYPE,
            total_crashes

        FROM yearly_crash_types

        WHERE crash_rank = 1

        ORDER BY year;
        """
        ,

        "11. Day of the week with the highest average crashes per hour":
        """
            WITH hourly_crashes AS
        (
            SELECT 
                CRASH_DAY_OF_WEEK,
                CRASH_HOUR,
                COUNT(*) AS total_crashes
            FROM crash_data
            WHERE CRASH_DAY_OF_WEEK IS NOT NULL
            AND CRASH_HOUR IS NOT NULL
            GROUP BY CRASH_DAY_OF_WEEK, CRASH_HOUR
        ),

        daily_average AS
        (
            SELECT 
                CRASH_DAY_OF_WEEK,

                ROUND(
                    AVG(total_crashes),
                    2
                ) AS avg_crashes_per_hour

            FROM hourly_crashes

            GROUP BY CRASH_DAY_OF_WEEK
        )

        SELECT 

            CASE

                WHEN CRASH_DAY_OF_WEEK = 1 THEN 'Sunday'
                WHEN CRASH_DAY_OF_WEEK = 2 THEN 'Monday'
                WHEN CRASH_DAY_OF_WEEK = 3 THEN 'Tuesday'
                WHEN CRASH_DAY_OF_WEEK = 4 THEN 'Wednesday'
                WHEN CRASH_DAY_OF_WEEK = 5 THEN 'Thursday'
                WHEN CRASH_DAY_OF_WEEK = 6 THEN 'Friday'
                WHEN CRASH_DAY_OF_WEEK = 7 THEN 'Saturday'

            END AS day_name,

            avg_crashes_per_hour

        FROM daily_average

        ORDER BY avg_crashes_per_hour DESC
        LIMIT 1;
        """
        ,

        "12. Group hours into buckets (Morning, Afternoon, Evening, Night)for high-risk time slots and  bucket with highest injury crashes":
        """
        WITH time_bucket_analysis AS
        (
            SELECT
                CASE

                    WHEN CRASH_HOUR BETWEEN 6 AND 11
                    THEN 'Morning'

                    WHEN CRASH_HOUR BETWEEN 12 AND 16
                    THEN 'Afternoon'

                    WHEN CRASH_HOUR BETWEEN 17 AND 20
                    THEN 'Evening'

                    ELSE 'Night'

                END AS time_bucket,

                SUM(INJURIES_TOTAL) AS total_injuries

            FROM crash_data

            GROUP BY time_bucket
        )
        SELECT
            time_bucket,
            total_injuries

        FROM time_bucket_analysis

        ORDER BY total_injuries DESC

        LIMIT 1;
        """
    ,

        "13. Top 3 contributing causes for each crash type":
        """
        SELECT
            CRASH_TYPE,
            PRIM_CONTRIBUTORY_CAUSE,
            COUNT(*) AS total_crashes

        FROM crash_data

        WHERE PRIM_CONTRIBUTORY_CAUSE IS NOT NULL

        GROUP BY
            CRASH_TYPE,
            PRIM_CONTRIBUTORY_CAUSE

        ORDER BY total_crashes DESC

        LIMIT 3;
        """
    ,

        "14. Year-over-year growth rate of crashes":
        """
        WITH yearly_crashes AS
        (
            SELECT 
                year,
                COUNT(*) AS total_crashes
            FROM crash_data
            WHERE year IS NOT NULL
            GROUP BY year
        ),

        growth_analysis AS
        (
            SELECT 
                year,
                total_crashes,

                LAG(total_crashes) OVER
                (
                    ORDER BY year
                ) AS previous_year_crashes

            FROM yearly_crashes
        )
        SELECT 
            year,
            total_crashes,
            previous_year_crashes,

            ROUND(
                (
                    (total_crashes - previous_year_crashes)
                    * 100.0
                ) / previous_year_crashes,
                2
            ) AS growth_rate_percentage

        FROM growth_analysis
        WHERE previous_year_crashes IS NOT NULL
        ORDER BY year;
        """
    ,
        "15. Group nearby locations (round latitude & longitude to 2 decimal places) and Find top 10 zones with highest crashes":
        """
        WITH hotspot_zones AS
        (
            SELECT 
                ROUND(LATITUDE, 2) AS latitude_zone,
                ROUND(LONGITUDE, 2) AS longitude_zone,

                COUNT(*) AS total_crashes

            FROM crash_data

            WHERE LATITUDE IS NOT NULL
            AND LONGITUDE IS NOT NULL

            GROUP BY 
                ROUND(LATITUDE, 2),
                ROUND(LONGITUDE, 2)
        ),

        zone_rank AS
        (
            SELECT 
                latitude_zone,
                longitude_zone,
                total_crashes,

                RANK() OVER
                (
                    ORDER BY total_crashes DESC
                ) AS crash_rank

            FROM hotspot_zones
        )

        SELECT 
            latitude_zone,
            longitude_zone,
            total_crashes,
            crash_rank

        FROM zone_rank

        WHERE crash_rank <= 10

        ORDER BY crash_rank;
        """
    }

    # Query selection
    selected_query = st.selectbox(
        "Choose a Query",
        list(queries.keys())
    )

    # Execute query
    query_result = get_data(
        queries[selected_query]
    )

    # Display result
    st.write("### Query Result")

    st.dataframe(query_result)

    # Show insight
    if selected_query == "1.Top 5 most dangerous combinations of weather and crash type":

       st.info(
           "Business Insight: Clear weather conditions increase crash risks significantly."
    )
    elif selected_query == "2. Top 10 streets with the highest number of injury crashes":

        st.info(
        "Business Insight: These streets experience the highest injury-related crashes and may require stricter traffic enforcement, speed monitoring, and improved road infrastructure."
    )

    elif selected_query == "3. Percentage of crashes that resulted in injuries for each crash type ":

        st.info(
        "Business Insight: This analysis helps identify crash types with the highest injury risk, allowing emergency response teams and policymakers to prioritize safety improvements."
    )

    elif selected_query == "4. Peak crash hour for each month":

        st.info(
        "Business Insight: Identifying peak crash hours helps traffic departments allocate police patrols, emergency services, and traffic management resources more effectively."
    )

    elif selected_query == "5. Top 5 primary causes of crashes during night time (CRASH_HOUR ≥ 18) ":

        st.info(
        "Business Insight: Understanding the major causes of night-time crashes helps in creating awareness campaigns and implementing targeted safety measures during late hours."
    )

    elif selected_query == "6. Average number of injuries in daylight vs darkness conditions":

        st.info(
        "Business Insight: Comparing injuries during daylight and darkness helps evaluate the impact of visibility conditions on crash severity."
    )

    elif selected_query == "7. Traffic control device type has the highest average injuries per crash":

        st.info(
        "Business Insight: This analysis identifies traffic control systems associated with severe crashes and supports infrastructure improvement decisions."
    )

    elif selected_query == "8. Top 5 locations (latitude/longitude) with the highest crash frequency":

        st.info(
        "Business Insight: These hotspot locations experience frequent crashes and may require better road design, traffic signals, or monitoring systems."
    )

    elif selected_query == "9. Top 5 streets with the highest injury rate and streets with more than 100 crashes":

        st.info(
        "Business Insight: Streets with high injury rates indicate dangerous traffic conditions and should be prioritized for road safety improvements."
    )

    elif selected_query == "10. Identify the most common crash type for each year.":

        st.info(
        "Business Insight: Tracking yearly crash patterns helps authorities understand changing traffic risks and evaluate the effectiveness of safety measures over time."
    )

    elif selected_query == "11. Day of the week with the highest average crashes per hour":

        st.info(
        "Business Insight: Identifying high-risk weekdays helps optimize staffing, traffic monitoring, and public safety planning."
    )

    elif selected_query == "12. Group hours into buckets (Morning, Afternoon, Evening, Night)for high-risk time slots and  bucket with highest injury crashes":

        st.info(
        "Business Insight: High-risk time slots indicate when severe crashes occur most frequently, helping emergency teams prepare resources during critical hours."
    )

    elif selected_query == "13. Top 3 contributing causes for each crash type":

        st.info(
        "Business Insight: Identifying major contributing causes helps traffic authorities implement targeted prevention strategies and driver awareness programs."
    )

    elif selected_query == "14. Year-over-year growth rate of crashes":

        st.info(
        "Business Insight: Crash growth trends help evaluate whether traffic safety initiatives are reducing or increasing accident rates over time."
    )

    elif selected_query == "15. Group nearby locations (round latitude & longitude to 2 decimal places) and Find top 10 zones with highest crashes":

        st.info(
        "Business Insight: High-crash zones highlight areas requiring urgent traffic safety interventions, improved infrastructure, and accident prevention measures."
    )

# =========================================================
# PAGE 4 : CREATOR INFO
# =========================================================

elif page == "Creator Info":

    st.title("👩‍💻 Creator of this Project")

    st.write("""
    **Developed by:** Harini

    **Skills:** Python, SQL, Data Analysis,Pandas,
    Streamlit
    """)