import pandas as pd
import math
import xgboost as xgb
import streamlit as st
import streamlit.components.v1 as components

from name_project import name_project
from latitude import latitude
from longtitude import longtitude

direct = ('Bắc', 'Đông', 'Đông - Bắc', 'Đông - Nam', 'Nam', 'Tây', 'Tây - Bắc', 'Tây - Nam')
polistic_value = ('Sổ đỏ', 'Sổ hồng', 'Hợp đồng mua bán', 'Chưa sổ')
furniture_value = ('Đầy đủ', 'Cơ bản', 'Cao cấp', 'Nguyên bản')
name_city = ('Hà Nội', 'Thành phố Hồ Chí Minh')
district_in_hanoi = ('Ba Đình', 'Bắc Từ Liêm', 'Cầu Giấy', 'Đan Phượng', 'Đông Anh', 'Đống Đa', 'Gia Lâm', 'Hà Đông', 'Hai Bà Trưng', 'Hoài Đức', 'Hoàn Kiếm', 'Hoàng Mai', 'Long Biên', 'Mê Linh', 'Nam Từ Liêm', 'Tây Hồ', 'Thạch Thất', 'Thanh Trì', 'Thanh Xuân')
district_in_tphcm = ('Bình Chánh', 'Bình Tân', 'Bình Thạnh', 'Gò Vấp', 'Hóc Môn', 'Nhà Bè', 'Phú Nhuận', 'Quận 1', 'Quận 2', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 6', 'Quận 7', 'Quận 8', 'Quận 9', 'Quận 10', 'Quận 11', 'Quận 12', 'Tân Bình', 'Tân Phú', 'Thủ Đức')
all_district = ('Ba Đình', 'Bắc Từ Liêm', 'Bình Chánh', 'Bình Tân', 'Bình Thạnh', 'Cầu Giấy', 'Đan Phượng', 'Đông Anh', 'Đống Đa', 'Gia Lâm', 'Gò Vấp', 'Hà Đông', 'Hai Bà Trưng', 'Hoài Đức', 'Hoàn Kiếm', 'Hoàng Mai', 'Hóc Môn', 'Long Biên', 'Mê Linh', 'Nam Từ Liêm', 'Nhà Bè', 'Phú Nhuận', 'Quận 1', 'Quận 2', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 6', 'Quận 7', 'Quận 8', 'Quận 9', 'Quận 10', 'Quận 11', 'Quận 12', 'Tân Bình', 'Tân Phú', 'Tây Hồ', 'Thạch Thất', 'Thanh Trì', 'Thanh Xuân', 'Thủ Đức')
def take_length(x, y):
    #data la vi tri ubnd
    ubnd_HN = [21.04542637226397, 105.83893178229242]
    ubnd_SN = [10.776813940162203, 106.70095053691294]
    length = round(math.sqrt((x - ubnd_HN[0])**2 + (y - ubnd_HN[1])**2), 4)*100
    if (length > 200):
        length = round(math.sqrt((x - ubnd_SN[0])**2 + (y - ubnd_SN[1])**2), 4)*100
    return length
def main():
    # load model
    model = xgb.XGBRegressor()
    model.load_model('xgb_model.json')

    polistic_encoder = 0
    furniture_encoder = 0
    district_encoder = 0
    house_direct_encoder = 0
    balcony_direct_encoder = 0
    name_project_encoder = 0
    html_temp="""
        <div style="background-color: lightblue; padding: 16px;">
            <h2 style="color:black; text-align: center; width: 41.5rem;">The Apartment Price Prediction Web</h2>
        </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    hide_spinner_style = """
        <style>
        button.step-down, button.step-up{
            display: none;
        }
        div.css-1hynsf2.esravye2>div>div {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            &[aria-label="District"] {
                display: grid;
                column-gap: 10px;
                grid-template-columns: 20% 20% 20% 20% 20%;
            }
        }
        </style>
    """
    st.markdown(hide_spinner_style, unsafe_allow_html=True)
    st.markdown("You can search for information about the estate project on Google or below here")
    components.iframe("https://app.powerbi.com/reportEmbed?reportId=76705c19-bc63-4366-8431-112bba4fd8be&autoAuth=true&ctid=06f1b89f-07e8-464f-b408-ec1b45703f31", height=400, width=704)

    # Get the Area input from the user
    area = st.number_input("Area", format="%.2f", min_value=0.0, step=0.01, value=0.0)
    # Validate if the number is positive
    if area < 0:
        st.error("Please enter a positive number.")
    # Display the entered number
    st.write("Entered area:", round(area, 2))

    col1, col2 = st.columns(2)
    with col1:
        house_direct = st.radio(
            "House direct",
            options=direct
        )
         # Display the entered
        st.write("Entered house direct:", house_direct)
    house_direct_encoder = direct.index(house_direct)
    with col2:
        balcony_direct = st.radio(
            "Balcony direct",
            options=direct
        )
         # Display the entered
        st.write("Entered balcony direct:", balcony_direct)
    balcony_direct_encoder = direct.index(house_direct)

    col3, col4 = st.columns(2)
    with col3:
        # Get the Number Bedrooms input from the user
        number_bedrooms = st.number_input("Number bedrooms", min_value=0, step=1, value=0)
        # Validate if the number is positive
        if number_bedrooms < 0:
            st.error("Please enter a positive number.")
        # Display the entered number
        st.write("Entered number bedrooms:", number_bedrooms)
    with col4:
        # Get the Number Toilets input from the user
        number_toilets = st.number_input("Number toilets", min_value=0, step=1, value=0)
        # Validate if the number is positive
        if number_toilets < 0:
            st.error("Please enter a positive number.")
        # Display the entered number
        st.write("Entered number toilets:", number_toilets)
    
    col5, col6 = st.columns(2)
    with col5:
        polistic = st.radio(
            "Polistic",
            options=polistic_value
        )
         # Display the entered
        st.write("Entered polistic:", polistic)
    if polistic == 'Sổ đỏ':
        polistic_encoder = 2
    if polistic == 'Sổ hồng':
        polistic_encoder = 2
    if polistic == 'Hợp đồng mua bán':
        polistic_encoder = 1
    if polistic == 'Chưa sổ':
        polistic_encoder = 0
    with col6:
        furniture = st.radio(
            "Furniture",
            options=furniture_value
        )
         # Display the entered
        st.write("Entered furniture:", furniture)
    if furniture == 'Đầy đủ':
        furniture_encoder = 2
    if furniture == 'Cơ bản':
        furniture_encoder = 1
    if furniture == 'Cao cấp':
        furniture_encoder = 0
    if furniture == 'Nguyên bản':
        furniture_encoder = 3

    project = st.selectbox('Name project', name_project)
    # Display the entered number
    st.write('Entered name project:', project)
    if project == 'Can ho D Lusso':
        name_project_encoder = 79
    if project == 'D. El Dorado':
        name_project_encoder = 262
    if project == 'D. El Dorado II':
        name_project_encoder = 263
    if project == 'D. Le Pont D or - Hoang Cau':
        name_project_encoder = 264
    if project == 'D. Le Roi Soleil':
        name_project_encoder = 265
    if project == 'D Edge Thao Dien':
        name_project_encoder = 266
    if project == 'Vinhomes D Capitale':
        name_project_encoder = 1024
    else:
        name_project_encoder = name_project.index(project)
    latitude_of_project = latitude[name_project_encoder]
    longtitude_of_project = longtitude[name_project_encoder]
    distance_to_UBND = take_length(latitude_of_project, longtitude_of_project)

    col7, col8 = st.columns(2)
    with col7:
        # Get the Number apartment of the project input from the user
        project_apartment_number = st.number_input("Number apartment of the project", min_value=0, step=1, value=0)
        # Validate if the number is positive
        if project_apartment_number < 0:
            st.error("Please enter a positive number.")
        # Display the entered number
        st.write("Entered number apartment of the project:", project_apartment_number)
    with col8:
        # Get the Number building of the project input from the user
        project_building_number = st.number_input("Number building of the project", min_value=0, step=1, value=0)
        # Validate if the number is positive
        if project_building_number < 0:
            st.error("Please enter a positive number.")
        # Display the entered number
        st.write("Entered number building of the project:", project_building_number)

    city = st.radio("Choose the city", options=name_city)
    if city == 'Hà Nội':
        district = st.radio(
            "District",
            options=district_in_hanoi
        )
         # Display the entered
        st.write("Entered district:", district)
    if city == 'Thành phố Hồ Chí Minh':
        district = st.radio(
            "District",
            options=district_in_tphcm
        )
         # Display the entered
        st.write("Entered district:", district)
    district_encoder = all_district.index(district)

    col9, col10 = st.columns(2)
    with col9:
        # Get the Min price of the project input from the user
        min_price_of_the_project = st.number_input("Min price of the project", format="%.2f", min_value=0.0, step=0.01, value=0.0)
        # Validate if the number is positive
        if min_price_of_the_project < 0:
            st.error("Please enter a positive number.")
        # Display the entered number
        st.write("Entered min price of the project:", round(min_price_of_the_project, 2))
    with col10:
        # Get the Max price of the project input from the user
        max_price_of_the_project = st.number_input("Max price of the project", format="%.2f", min_value=0.0, step=0.01, value=0.0)
        # Validate if the number is positive
        if max_price_of_the_project < 0:
            st.error("Please enter a positive number.")
        if 0 < max_price_of_the_project < min_price_of_the_project:
            st.error("Max price of the project must be greater than min price of the project")
        # Display the entered number
        st.write("Entered max price of the project:", round(max_price_of_the_project, 2))

    col11, col12 = st.columns(2)
    with col11:
        # Get the Min area of the project input from the user
        min_area_of_the_project = st.number_input("Min area of the project", format="%.2f", min_value=0.0, step=0.01, value=0.0)
        # Validate if the number is positive
        if min_area_of_the_project < 0:
            st.error("Please enter a positive number.")
        # Display the entered number
        st.write("Entered min area of the project:", round(min_area_of_the_project, 2))
    with col12:
        # Get the Max area of the project input from the user
        max_area_of_the_project = st.number_input("Max area of the project", format="%.2f", min_value=0.0, step=0.01, value=0.0)
        # Validate if the number is positive
        if max_area_of_the_project < 0:
            st.error("Please enter a positive number.")
        if 0 < max_area_of_the_project < min_area_of_the_project:
            st.error("Max area of the project must be greater than min area of the project")
        # Display the entered number
        st.write("Entered max area of the project:", round(max_area_of_the_project, 2))
    col13, col14, col15 = st.columns(3)
    with col13:
        # Get the Number Hospitals input from the user
        number_hospitals = st.number_input("Number of hospitals around 1 km", min_value=0, step=1, value=0)
        # Validate if the number is positive
        if number_hospitals < 0:
            st.error("Please enter a positive number.")
        # Display the entered number
        st.write("Entered number hospitals:", number_hospitals)
    with col14:
        # Get the Number Schools input from the user
        number_schools = st.number_input("Number of schools around 1 km", min_value=0, step=1, value=0)
        # Validate if the number is positive
        if number_schools < 0:
            st.error("Please enter a positive number.")
        # Display the entered number
        st.write("Entered number schools:", number_schools)
    with col15:
        # Get the Number Banks input from the user
        number_banks = st.number_input("Number of banks around 1 km", min_value=0, step=1, value=0)
        # Validate if the number is positive
        if number_banks < 0:
            st.error("Please enter a positive number.")
        # Display the entered number
        st.write("Entered number banks:", number_banks)

    # Prediction
    new_data = {
        'area': [area],
        'house_direct_encoded': [house_direct_encoder],
        'balcony_direct_encoded': [balcony_direct_encoder],
        'n_rooms': [number_bedrooms],
        'n_toilets': [number_toilets],
        'polistic_encoded': [polistic_encoder],
        'furniture_encoded': [furniture_encoder],
        'name_project_encoded': [name_project_encoder],
        'project_apartment_number': [project_apartment_number],
        'project_building_number': [project_building_number],
        'district_encoded': [district_encoder],
        'min_price_of_project': [min_price_of_the_project],
        'max_price_of_project': [max_price_of_the_project],
        'min_area_of_project': [min_area_of_the_project],
        'max_area_of_project': [max_area_of_the_project],
        'x': [latitude_of_project],
        'y': [longtitude_of_project],
        'distance': [distance_to_UBND],
        'n_hospitals': [number_hospitals],
        'n_schools': [number_schools],
        'n_banks': [number_banks]
    }
    # Create a DataFrame from the sample data
    new_data = pd.DataFrame(new_data)

    try:
        if st.button('Predict'):
            if new_data['area'][0] == 0:
                st.warning("Something went wrong, please try again!")
            else:
                pred = model.predict(new_data)
                if pred > 0:
                    st.balloons()
                    st.success("The apartment has price about {:.2f}".format(pred[0]))
                else:
                    st.warning("You can't able to predict this apartment")
    except:
        st.warning("Something went wrong, please try again!")

if __name__ == '__main__':
    main()
