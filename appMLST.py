import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay, PrecisionRecallDisplay
from sklearn.metrics import precision_score, recall_score

def main():
    st.title("Binary Classification Web App")
    st.sidebar.title("Binary Classification Web App")
    st.markdown("Are your mushroom edible or poisonous? 🍄")
    st.sidebar.markdown("Are your mushroom edible or poisonous? 🍄")

    @st.cache_data(persist=True)
    def load_data():
        data = pd.read_csv(r'C:\Users\glawb\Downloads\mushrooms.csv')
        label = LabelEncoder()
        for col in data.columns:
            data[col] = label.fit_transform(data[col])
        return data
    
    @st.cache_data(persist=True)
    def split(df):
        y = df.type
        x = df.drop(columns=['type'])
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
        return x_train, x_test, y_train, y_test

    def plot_metrics(metrics_list):
        if 'Confusion Matrix' in metrics_list:
            st.subheader("Confusion Matrix")
            fig, ax = plt.subplots()
            ConfusionMatrixDisplay.from_estimator(model, x_test, y_test, display_labels=class_names, ax=ax)
            st.pyplot(fig)
        
        if 'ROC Curve' in metrics_list:
            st.subheader("ROC Curve")
            fig, ax = plt.subplots()
            RocCurveDisplay.from_estimator(model, x_test, y_test, ax=ax)
            st.pyplot(fig)
        
        if 'Precision-Recall Curve' in metrics_list:
            st.subheader('Precision-Recall Curve')
            fig, ax = plt.subplots()
            PrecisionRecallDisplay.from_estimator(model, x_test, y_test, ax=ax)
            st.pyplot(fig)

    df = load_data()
    x_train, x_test, y_train, y_test = split(df)
    class_names = ['edible', 'poisonous']
    st.sidebar.subheader("Choose Classifier")
    classifier = st.sidebar.selectbox("Classifier", ("Support Vector Machine (SVM)", "Logistic Regression", "Random Forest"))

    if classifier == 'Support Vector Machine (SVM)':
        st.sidebar.subheader("Model Hyperparameters")
        C = st.sidebar.number_input('C (Regularization parameter)', 0.01, 10.0, step=0.01, key='C')
        kernel = st.sidebar.radio('Kernel', ('rbf', 'linear'), key='kernel')
        gamma = st.sidebar.radio('Gamma (Kernel Coefficient)', ('scale','auto'), key='gamma')

        metrics = st.sidebar.multiselect('What metric to plot?', ('Confusion Matrix','ROC Curve','Precision-Recall Curve'))

        if st.sidebar.button('Classify', key='classify'):
            st.subheader('Support Vector Machine (SVM) Results')
            model = SVC(C=C, kernel=kernel, gamma=gamma)
            model.fit(x_train,y_train)
            accuracy = model.score(x_test, y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy: ", round(accuracy, 2))
            st.write("Precision: ", precision_score(y_test, y_pred, labels=[0,1]).round(2))
            st.write("Recall: ", recall_score(y_test, y_pred, labels=[0,1]).round(2))
            plot_metrics(metrics)

    if classifier == 'Logistic Regression':
        st.sidebar.subheader("Model Hyperparameters")
        C = st.sidebar.number_input('C (Regularization parameter)', 0.01, 10.0, step=0.01, key='C')
        max_iter = st.sidebar.slider("Maximun number of iterations", 100, 500, key='max_iter')

        metrics = st.sidebar.multiselect('What metric to plot?', ('Confusion Matrix','ROC Curve','Precision-Recall Curve'))

        if st.sidebar.button('Classify', key='classify'):
            st.subheader('Logistic Regression Results')
            model = LogisticRegression(C=C, max_iter=max_iter)
            model.fit(x_train,y_train)
            accuracy = model.score(x_test, y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy: ", round(accuracy, 2))
            st.write("Precision: ", precision_score(y_test, y_pred, labels=[0,1]).round(2))
            st.write("Recall: ", recall_score(y_test, y_pred, labels=[0,1]).round(2))
            plot_metrics(metrics)

    if classifier == 'Random Forest':
        st.sidebar.subheader("Model Hyperparameters")
        n_estimators = st.sidebar.number_input("The number of trees in the forest", 100, 5000, step=10, key='n_estimators')
        max_depth = st.sidebar.number_input("The maximum depth of the tree", 1, 20, step=1, key='max_depth')
        bootstrap = st.sidebar.radio('Bootstrap smaples when building trees', (True, False), key='bootstrap')

        metrics = st.sidebar.multiselect('What metric to plot?', ('Confusion Matrix','ROC Curve','Precision-Recall Curve'))

        if st.sidebar.button('Classify', key='classify'):
            st.subheader('Random Forest Results')
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, bootstrap=bootstrap, n_jobs=-1)
            model.fit(x_train,y_train)
            accuracy = model.score(x_test, y_test)
            y_pred = model.predict(x_test)
            st.write("Accuracy: ", round(accuracy, 2))
            st.write("Precision: ", precision_score(y_test, y_pred, labels=[0,1]).round(2))
            st.write("Recall: ", recall_score(y_test, y_pred, labels=[0,1]).round(2))
            plot_metrics(metrics)

    if st.sidebar.checkbox("Show raw data", False):
        st.subheader("Mushroom Data Set (Classification)")
        st.write(df)


if __name__ == '__main__':
    main()


