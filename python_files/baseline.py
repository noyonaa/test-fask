import sys
import pandas as pd
import plotly.express as px

def baseline(company_id, crop_id, choice):
    print(company_id, crop_id, choice)
    data = pd.read_csv("csvfiles/baseline_YN.csv")
    data = data[data['crop_id'] == crop_id]
    data = data[data['company_id'] == company_id]

    if choice == 1:
        data['baseline'] = data['baseline'].replace({'Y': 'Before', 'N': 'After'})
        baseline_order = ['Before', 'After']
        fig = px.bar(data, x='farm_name', y='total_yield', color='baseline',
                     color_discrete_sequence=['red', 'green'],
                     category_orders={'baseline': baseline_order})
        fig.update_layout(
            title='Total Yield for chilli in farms, Before Vs After',
            xaxis_title='Farm Name',
            yaxis_title='Total Yield',
            bargap=0.3,
            barmode='group',
            height=400,
            width=1100
        )
        fig.write_html("htmls/fig1.html")

    elif choice == 2:
        data['baseline'] = data['baseline'].replace({'Y': 'Before', 'N': 'After'})
        baseline_order = ['Before', 'After']
        fig = px.bar(data, x='farm_name', y='total_cost', color='baseline',
                     color_discrete_sequence=['red', 'green'],
                     category_orders={'baseline': baseline_order})
        fig.update_layout(
            title='Total Cost in farms, Before Vs After',
            xaxis_title='Farm Name',
            yaxis_title='Total Cost',
            bargap=0.3,
            barmode='group',
            height=400,
            width=1100
        )
        fig.write_html("htmls/fig1.html")

    elif choice == 3:
        data['baseline'] = data['baseline'].replace({'Y': 'Before', 'N': 'After'})
        baseline_order = ['Before', 'After']
        fig = px.bar(data, x='farm_name', y='fertilizer_cost', color='baseline',
                     color_discrete_sequence=['red', 'green'],
                     category_orders={'baseline': baseline_order})
        fig.update_layout(
            title='Fertilizer Cost in farms, Before Vs After',
            xaxis_title='Farm Name',
            yaxis_title='Fertilizer Cost',
            bargap=0.3,
            barmode='group',
            height=400,
            width=1100
        )
        fig.write_html("htmls/fig1.html")

    elif choice == 4:
        data['baseline'] = data['baseline'].replace({'Y': 'Before', 'N': 'After'})

        baseline_order = ['Before', 'After']
        fig = px.bar(data, x='farm_name', y='labout_cost', color='baseline',
                     color_discrete_sequence=['red', 'green'],
                     category_orders={'baseline': baseline_order})
        fig.update_layout(
            title='Labour Cost for chilli in farms, Before Vs After',
            xaxis_title='Farm Name',
            yaxis_title='Labour Cost',
            bargap=0.3,
            barmode='group',
            height=400,
            width=1100
        )
        fig.write_html("htmls/fig1.html")

    elif choice == 5:
        data['baseline'] = data['baseline'].replace({'Y': 'Before', 'N': 'After'})

        baseline_order = ['Before', 'After']
        fig = px.bar(data, x='farm_name', y='land_preparation_cost', color='baseline',
                     color_discrete_sequence=['red', 'green'],
                     category_orders={'baseline': baseline_order})
        fig.update_layout(
            title='Land Preparation Cost for chilli in farms, Before Vs After',
            xaxis_title='Farm Name',
            yaxis_title='Land Preparation Cost',
            bargap=0.3,
            barmode='group',
            height=400,
            width=1100
        )
        fig.write_html("htmls/fig1.html")

    elif choice == 6:
        data['baseline'] = data['baseline'].replace({'Y': 'Before', 'N': 'After'})

        baseline_order = ['Before', 'After']
        fig = px.bar(data, x='farm_name', y='pest_disease_cost', color='baseline',
                     color_discrete_sequence=['red', 'green'],
                     category_orders={'baseline': baseline_order})
        fig.update_layout(
            title='Pest and disease control cost for chilli in farms, Before Vs After',
            xaxis_title='Farm Name',
            yaxis_title='Pest and disease control Cost',
            bargap=0.3,
            barmode='group',
            height=400,
            width=1100
        )
        fig.write_html("htmls/fig1.html")


    elif choice == 7:
        data['baseline'] = data['baseline'].replace({'Y': 'Before', 'N': 'After'})

        baseline_order = ['Before', 'After']
        fig = px.bar(data, x='farm_name', y='net_profit', color='baseline',
                     color_discrete_sequence=['red', 'green'],
                     category_orders={'baseline': baseline_order})
        fig.update_layout(
            title='Net Profit for chilli in farms, Before Vs After',
            xaxis_title='Farm Name',
            yaxis_title='Net profit',
            bargap=0.3,
            barmode='group',
            height=400,
            width=1100
        )
        fig.write_html("htmls/fig1.html")
    

    

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 companyplans.py <company_id> <crop_id> <choice>")
        sys.exit(1)

    company_id = int(sys.argv[1])
    crop_id = int(sys.argv[2])
    choice = int(sys.argv[3])

    baseline(company_id, crop_id, choice)
