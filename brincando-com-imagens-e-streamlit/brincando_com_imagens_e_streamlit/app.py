import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from PIL import Image

RED = 0
GREEN = 1 
BLUE = 2


st.write('## Brincando com imagens')

st.sidebar.write('### Configurações')

uploaded_file = st.sidebar.file_uploader("Escolha uma imagem", 
    type=['png','jpg']
)

# is_black_and_white = st.sidebar.checkbox('Preto e branco?')


if uploaded_file is not None:
    image_source = Image.open(uploaded_file)

    image = np.asarray(image_source)
    

    col1, col2 = st.columns(2)

    with col1:
        # image_gray = np.copy(image)        
        # image_gray = np.mean(image_gray, axis=2) / 255    
        st.write('## Imagem Original')

        st.image(image)
        # st.write('### Média')
        # st.image(image_gray)

    with col2:
        pesos = [0.2126, 0.7152, 0.0722]
        image_gray_corr = np.copy(image)   
        image_gray_corr = np.array(image_gray_corr * pesos, dtype=np.uint8)
        image_gray_corr = np.array(np.sum(image_gray_corr, axis=2), dtype=np.uint8)

        st.write('## Tons de Cinza')
        # st.latex(r'''
        #     Y_{linear} = 0.2126R_{linear} 
        #         + 0.7152G_{linear}
        #         + 0.0722B_{linear}
        # ''')
        st.image(image_gray_corr)

    option = st.sidebar.selectbox(
        'Qual transformação?',
        (None, 'negativo', 'log', 'power-law (gamma)'),
    )

    image_aux = np.copy(image_gray_corr)

    st.write(f'## {option}'.upper())

    if option == 'negativo':
        image_aux = 255 - image_aux
    elif option == 'log':
        st.sidebar.latex(r'''
            s = c \times log(1 + r)
        ''')

        c = st.sidebar.slider(
            'c',
            0, 100, 25
        )

        st.write('c:', c)

        image_aux_arr = c * (np.log(image_aux + 1))
        image_aux = Image.fromarray(image_aux_arr.astype(np.uint8)).convert('L')

        fig, ax = plt.subplots()
        ax.hist(image_aux_arr.astype(np.uint8).flatten(), bins=20)
        st.sidebar.pyplot(fig)

    elif option == 'power-law (gamma)':
        st.sidebar.latex(r'''
            s = c \times r^\gamma
        ''')

        c = st.sidebar.slider(
            'c',
            0, 255, 25
        )

        gamma = st.sidebar.slider(
            'gamma',
            0.0, 25.0, 1.0, 0.02
        )

        st.write(f"c: {c}, gamma: {gamma}")

        image_aux_arr = c * ((image_aux/255) ** gamma)
        image_aux = Image.fromarray(image_aux_arr.astype(np.uint8)).convert('L')

        fig, ax = plt.subplots()
        ax.hist(image_aux_arr.astype(np.uint8).flatten(), bins=5)
        st.sidebar.pyplot(fig)
    # image_aux_arr.astype(int)
    # st.write(image_aux_arr.astype)
    st.image(image_aux)


    # elif(option == 'Transformação em (log)'):
        
    #     c = st.sidebar.slider('c', 0, 130, 25)
    #     if color == 'tons de cinza':
    #         log_image_arr = c * (np.log(gray_arr + 1))
    #         image = Image.fromarray(log_image_arr).convert('L')
    #         # image = Image.fromarray(255 - gray_arr).convert('L') 
    #     else:
    #         image[:,:,0] = c * (np.log(image[:,:,0] + 1))
    #         image[:,:,1] = c * (np.log(image[:,:,1] + 1))
    #         image[:,:,2] = c * (np.log(image[:,:,2] + 1))
    #         image = Image.fromarray(image).convert('L')

    # image_aux
    option = st.sidebar.selectbox(
        'Qual o nível de cores?',
        (2, 4, 8, 16, 32, 64, 128, 192, 256),
    )

    image_aux = np.copy(image_gray_corr)

    st.write(f'## Imagem com {option} cores'.upper())
    
    def num_cores(q_cor, imag_aux):
        div_cores = (256 / q_cor)
        print(div_cores)
        print(f'color: {q_cor}')
        for i in range(q_cor):
            if i == 0:
                imag_aux[imag_aux <= div_cores] = 0
            elif i == q_cor - 1:
                imag_aux[imag_aux >= (div_cores * i)] = 255
            else:
                imag_aux[(imag_aux > ((i * div_cores) - 1)) & 
                        (imag_aux < ((i + 1) * div_cores))] = div_cores * i

    num_cores(option, image_aux)

    st.image(image_aux)