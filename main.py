import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageDraw

# Set the Streamlit app background color to sky blue
st.markdown(
    """
    <style>
    body {
        background-color: #d6e9ff;
        color: #0d0469;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Image Transformation")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    transform_type = st.selectbox("Select Transformation", ["None", "Rotation", "Scaling", "Translation", "Shearing", "Affine"])

    if transform_type == "Rotation":
        angle = st.slider("Rotation Angle (degrees)", -360, 360, 0)
        if st.button("Apply Rotation"):
            image = Image.open(uploaded_image)
            transformed_image = image.rotate(angle)
            st.image(transformed_image, caption="Transformed Image", use_column_width=True)

    elif transform_type == "Scaling":
        scale_factor_x = st.slider("Scale Factor X", 0.1, 3.0, 1.0)
        scale_factor_y = st.slider("Scale Factor Y", 0.1, 3.0, 1.0)
        if st.button("Apply Scaling"):
            image = Image.open(uploaded_image)
            new_width = int(image.width * scale_factor_x)
            new_height = int(image.height * scale_factor_y)
            transformed_image = image.resize((new_width, new_height))
            st.image(transformed_image, caption="Transformed Image", use_column_width=True)

    elif transform_type == "Translation":
        x_translate = st.slider("X Translation", -100, 100, 0)
        y_translate = st.slider("Y Translation", -100, 100, 0)
        if st.button("Apply Translation"):
            image = Image.open(uploaded_image)
            width, height = image.size
            new_width = width + x_translate
            new_height = height + y_translate
            transformed_image = Image.new("RGB", (new_width, new_height), (255, 255, 255))
            transformed_image.paste(image, (x_translate, y_translate))
            st.image(transformed_image, caption="Transformed Image", use_column_width=True)

    elif transform_type == "Shearing":
        x_shear = st.slider("X Shearing", -1.0, 1.0, 0.0)
        y_shear = st.slider("Y Shearing", -1.0, 1.0, 0.0)
        if st.button("Apply Shearing"):
            image = Image.open(uploaded_image)
            shear_matrix = [1, x_shear, 0, y_shear, 1, 0]
            transformed_image = image.transform(image.size, Image.AFFINE, shear_matrix, resample=Image.BILINEAR)
            st.image(transformed_image, caption="Transformed Image", use_column_width=True)

    elif transform_type == "Affine":
        st.markdown("Input 2x3 affine transformation matrix:")
        a = st.number_input("Scale X", value=1.0)
        b = st.number_input("Shear X", value=0.0)
        c = st.number_input("Translate X", value=0.0)
        d = st.number_input("Shear Y", value=0.0)
        e = st.number_input("Scale Y", value=1.0)
        f = st.number_input("Translate Y", value=0.0)

        if st.button("Apply Affine Transformation"):
            image = Image.open(uploaded_image)
            width, height = image.size
            transformed_image = Image.new("RGB", (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(transformed_image)

            for y in range(height):
                for x in range(width):
                    new_x = int(a * x + b * y + c)
                    new_y = int(d * x + e * y + f)
                    if 0 <= new_x < width and 0 <= new_y < height:
                        pixel = image.getpixel((new_x, new_y))
                        draw.point((x, y), fill=pixel)

            st.image(transformed_image, caption="Transformed Image", use_column_width=True)