import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Set the display format for floating-point numbers
pd.options.display.float_format = '{:,.2f}'.format

# Read the CSV file into a DataFrame
boston_df = pd.read_csv('data/boston.csv', index_col=0)

# Explore the data
print(boston_df.shape)
print(boston_df.columns)
print(boston_df.isna().values.any())
print(boston_df.duplicated().values.any())
print(boston_df.describe())

# Bar + KDE Chart: House Prices
sns.displot(
    boston_df.PRICE,
    bins=50,
    aspect=2,
    kde=True
)
plt.title(
    '1970s Home Values in Boston (Average: $'
    f'{(1000*boston_df.PRICE.mean()):.2f})'
)
plt.xlabel("Price in $1000's")
plt.ylabel('Number of Homes')
plt.show()

# Bar + KDE Chart: Distance to Employment
sns.displot(
    boston_df.DIS,
    bins=50,
    aspect=2,
    kde=True
)
plt.title(
    f'Distance to Employment Centres (Average: {(boston_df.DIS.mean()):.1f})'
)
plt.xlabel('Weighted Distance to 5 Boston Employment Centres')
plt.ylabel('Number of Homes')
plt.show()

# Bar + KDE Chart: Number of Rooms
sns.displot(
    boston_df.RM,
    aspect=2,
    kde=True
)
plt.title(
    f'Distribution of Rooms in Boston (Average: {boston_df.RM.mean():.2})'
)
plt.xlabel('Average Number of Rooms')
plt.ylabel('Number of Homes')
plt.show()

# Bar + KDE Chart: Access to Highways
sns.displot(
    boston_df.RAD,
    aspect=2,
    kde=True
)
plt.xlabel('Accessibility to Highways')
plt.ylabel('Number of Homes')
plt.show()

# Count the number of homes with river access
river_access = boston_df['CHAS'].value_counts()

# Bar Chart: Number of Properties Located Next to the River
river_bar = px.bar(
    x=['No', 'Yes'],
    y=river_access.values,
    color=river_access.values,
    color_continuous_scale=px.colors.sequential.haline
)
river_bar.update_layout(
    xaxis_title='Property Located Next to the River?',
    yaxis_title='Number of Homes',
    coloraxis_showscale=False
)
river_bar.show()

# Pair Plot
sns.pairplot(boston_df)
plt.show()

# Join Plot: Distance from Employment vs Pollution
with sns.axes_style('darkgrid'):
    sns.jointplot(
        x=boston_df['DIS'],
        y=boston_df['NOX'],
        height=8,
        kind='scatter',
        joint_kws={'alpha': 0.5}
    )
plt.show()

# Join Plot: Proportion of Non-Retail Industry vs Pollution
with sns.axes_style('darkgrid'):
    sns.jointplot(
        x=boston_df.NOX,
        y=boston_df.INDUS,
        color='red',
        height=7,
        joint_kws={'alpha': 0.5}
    )
plt.show()

# Join Plot: % of Lower Income Population vs Average Number of Rooms
with sns.axes_style('darkgrid'):
    sns.jointplot(
        x=boston_df['LSTAT'],
        y=boston_df['RM'],
        color='green',
        height=7,
        joint_kws={'alpha': 0.5}
    )
plt.show()

# Join Plot: % of Lower Income Population vs Home Price
with sns.axes_style('darkgrid'):
    sns.jointplot(
        x=boston_df.LSTAT,
        y=boston_df.PRICE,
        color='purple',
        height=7,
        joint_kws={'alpha': 0.5}
    )
plt.show()

# Join Plot: Number of Rooms vs Home Value
with sns.axes_style('whitegrid'):
    sns.jointplot(
        x=boston_df.RM,
        y=boston_df.PRICE,
        color='orange',
        height=7,
        joint_kws={'alpha': 0.5}
    )
plt.show()

# Define the target variable as the price of the homes
target = boston_df['PRICE']
# Define the features as all the other variables
features = boston_df.drop('PRICE', axis=1)

# Split the data into training and test sets,
# with 80% for training and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    features,
    target,
    test_size=0.2,
    random_state=10
)

# Calculate the percentage of training data out of the total data
train_pct = 100*len(X_train)/len(features)
print(f'Training data: {train_pct:.2f}%')

# Calculate the percentage of test data out of the total data
test_pct = 100*X_test.shape[0]/features.shape[0]
print(f'Test data: {test_pct:.2f}%')

# Create a linear regression model
regression = LinearRegression()
# Fit the model to the training data
regression.fit(X_train, y_train)

# Calculate the coefficient of determination (R-squared) for the model
r_squared = regression.score(X_train, y_train)
print(f'{r_squared:.2f}')

# Create a DataFrame with the regression coefficients for each feature
regression_coef = pd.DataFrame(
    data=regression.coef_, index=X_train.columns,
    columns=['Coefficient']
)
print(regression_coef)

# Calculate the price increase for an extra room in a property
extra_room_price = regression_coef.loc['RM'].values[0] * 1000
print(f'{extra_room_price:.2f}')

# Predict the price of the homes in the training data using the model
predicted_values = regression.predict(X_train)

# Calculate the residuals
residuals = (y_train - predicted_values)

# Scatter Plot: Regression of Actual vs Predicted Prices
plt.figure(dpi=100)
plt.scatter(x=y_train, y=predicted_values, c='indigo', alpha=0.6)
plt.plot(y_train, y_train, color='cyan')
plt.title('Actual vs Predicted Prices', fontsize=17)
plt.xlabel('Actual prices 1000s', fontsize=14)
plt.ylabel('Prediced prices 1000s', fontsize=14)
plt.show()

# Scatter Plot: Residuals vs Predicted Values
plt.figure(dpi=100)
plt.scatter(x=predicted_values, y=residuals, c='indigo', alpha=0.6)
plt.title('Residuals vs Predicted Values', fontsize=17)
plt.xlabel('Predicted Prices', fontsize=14)
plt.ylabel('Residuals', fontsize=14)
plt.show()

# Calculate the mean and the skewness of the residuals
residuals_mean = round(residuals.mean(), 2)
residuals_skew = round(residuals.skew(), 2)

# Histogram + KDE Chart: Residuals
sns.displot(residuals, kde=True, color='indigo')
plt.title(f'Residuals Skew ({residuals_skew}) Mean ({residuals_mean})')
plt.show()

# Calculate the skewness of the original prices
price_skew = boston_df['PRICE'].skew()

# Histogram + KDE Chart: Original Prices
sns.displot(boston_df['PRICE'], kde='kde')
plt.title(f'Skew: {price_skew:.2f}')
plt.show()

# Apply a log transformation to the original prices
log_price = np.log(boston_df['PRICE'])

# Histogram + KDE Chart: Log-transformed Prices
sns.displot(log_price, kde='kde')
plt.title(f'Skew: {log_price.skew():.2f}')
plt.show()

# Scatter Plot: Original Prices vs Log-transformed Prices
plt.figure(dpi=150)
plt.scatter(boston_df.PRICE, np.log(boston_df.PRICE))
plt.title('Mapping the Original Price to a Log Price')
plt.ylabel('Log Price')
plt.xlabel('Actual $ Price in 1000s')
plt.show()

# Define the new target variable as the log-transformed prices
new_target = np.log(boston_df['PRICE'])
# Define the features as all the other variables except the price
features = boston_df.drop('PRICE', axis=1)

# Split the data into training and test sets,
# with 80% for training and 20% for testing
X_train, X_test, log_y_train, log_y_test = train_test_split(
    features,
    new_target,
    test_size=0.2,
    random_state=10
)

# Create a linear regression model
log_regression = LinearRegression()
# Fit the model to the training data
log_regression.fit(X_train, log_y_train)

# Calculate the coefficient of determination (R-squared) for the model
log_r_squared = log_regression.score(X_train, log_y_train)
print(f'{log_r_squared:.2f}')

# Predict the log-transformed price of the
# homes in the training data using the model
log_predictions = log_regression.predict(X_train)
# Calculate the residuals
log_residuals = (log_y_train - log_predictions)

# Create a DataFrame with the regression coefficients for each feature
df_coef = pd.DataFrame(
    data=log_regression.coef_, index=X_train.columns, columns=['coef']
)
print(df_coef)

# Scatter Plot: Regression of Actual vs Predicted Prices (Log Prices)
plt.scatter(x=log_y_train, y=log_predictions, c='navy', alpha=0.6)
plt.plot(log_y_train, log_y_train, color='cyan')
plt.title('Actual vs Predicted Log Prices', fontsize=17)
plt.xlabel('Actual Log Prices', fontsize=14)
plt.ylabel('Prediced Log Prices', fontsize=14)
plt.show()

# Scatter Plot: Regression of Actual vs Predicted Prices
plt.figure(dpi=100)
plt.scatter(x=y_train, y=predicted_values, c='indigo', alpha=0.6)
plt.plot(y_train, y_train, color='cyan')
plt.title('Actual vs Predicted Prices', fontsize=17)
plt.xlabel('Actual prices 1000s', fontsize=14)
plt.ylabel('Prediced prices 1000s', fontsize=14)
plt.show()

# Scatter Plot: Residuals vs Predicted Values (Log Prices)
plt.scatter(x=log_predictions, y=log_residuals, c='navy', alpha=0.6)
plt.title('Residuals vs Fitted Values for Log Prices', fontsize=17)
plt.xlabel('Predicted Log Prices', fontsize=14)
plt.ylabel('Residuals', fontsize=14)
plt.show()

# Scatter Plot: Residuals vs Predicted Values
plt.figure(dpi=100)
plt.scatter(x=predicted_values, y=residuals, c='indigo', alpha=0.6)
plt.title('Residuals vs Predicted Values', fontsize=17)
plt.xlabel('Predicted Prices', fontsize=14)
plt.ylabel('Residuals', fontsize=14)
plt.show()

# Calculate the mean and the skewness of the log residuals
log_resid_mean = round(log_residuals.mean(), 2)
log_resid_skew = round(log_residuals.skew(), 2)

# Bar + KDE Chart: Residuals Skew and Mean (Log Price Model)
sns.displot(log_residuals, kde=True, color='navy')
plt.title(
    'Log price model: Residuals Skew '
    f'({log_resid_skew}) Mean ({log_resid_mean})'
)
plt.show()

# Bar + KDE Chart: Residuals Skew and Mean (Original Model)
sns.displot(residuals, kde=True, color='indigo')
plt.title(
    'Original model: Residuals Skew '
    f'({residuals_skew}) Mean ({residuals_mean})'
)
plt.show()

# Comparative of R-squared for both models (original and log)
print(f'{regression.score(X_test, y_test):.2}')
print(f'{log_regression.score(X_test, log_y_test):.2}')

# Create a DataFrame with the average values of each feature in the dataset
# Drop the price column from the dataset
features = boston_df.drop(['PRICE'], axis=1)
# Calculate the mean values of each feature
average_vals = features.mean().values
# Create a data frame with one row and columns as feature names
property_stats = pd.DataFrame(
    data=average_vals.reshape(1, len(features.columns)),
    columns=features.columns
)

# Make prediction
log_estimate = log_regression.predict(property_stats)[0]
# Convert the log price to a normal dollar value
dollar_est = np.exp(log_estimate) * 1000
print(f'${dollar_est:.2f}')

# Define Property Characteristics
next_to_river = True
nr_rooms = 8
students_per_classroom = 20
distance_to_town = 5
pollution = boston_df.NOX.quantile(q=0.75)
amount_of_poverty = boston_df.LSTAT.quantile(q=0.25)

# Set Property Characteristics
property_stats['RM'] = nr_rooms
property_stats['PTRATIO'] = students_per_classroom
property_stats['DIS'] = distance_to_town
property_stats['NOX'] = pollution
property_stats['LSTAT'] = amount_of_poverty
if next_to_river:
    property_stats['CHAS'] = 1
else:
    property_stats['CHAS'] = 0

# Make prediction
log_estimate = log_regression.predict(property_stats)[0]
# Convert the log price to a normal dollar value
dollar_est = np.exp(log_estimate) * 1000
print(f'${dollar_est:.2f}')
