import boto3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from operator import itemgetter


def metrics_reading(name,unit):
    response1 = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=name,
        Dimensions=[

            {
                'Name': 'InstanceId',
                'Value': 'i-0eb0378fa1e6fe0fd'
            },
        ],

        StartTime=datetime.now() - timedelta(hours=2),
        EndTime=datetime.now(),
        Period=300,
        Statistics=[
            'Average',
        ],
        Unit=unit
    )

    y1 = []
    x1 = []

    LatencyList1 = []
    for item in response1['Datapoints']:
        LatencyList1.append(item)

    LatencyList1 = sorted(LatencyList1, key=itemgetter('Timestamp'))


    for i in range(0, len(LatencyList1), 1):

        y1.append(LatencyList1[i]['Average'])
        x1.append(LatencyList1[i]['Timestamp'])

    return y1,x1

#################### PLOTTING ###############################3

#Getting CP Utilization for our instance
y1,x1 = metrics_reading('CPUUtilization', 'Percent')

#Getting Status Check Failed for our instance
y2,x2 = metrics_reading('StatusCheckFailed', 'Count')

#Getting Packets IN for our instance
y3,x3 = metrics_reading('NetworkIn', 'Bytes')

#Getting NetworkOut for our instance
y4,x4 = metrics_reading('NetworkOut','Bytes')

# Initialise the subplot function using number of rows and columns
figure, axis = plt.subplots(2, 2)

# For CPU utilization
axis[0, 0].plot(x1,y1)
axis[0, 0].set_title('CPU utilization')
axis[0, 0].set_ylabel('Average Percent %')

#for self status check
axis[0, 1].plot(x2,y2)
axis[0, 1].set_title('Status Check Failed')
axis[0, 1].set_ylabel('Count')

# For Network In
axis[1, 0].plot(x3,y3)
axis[1, 0].set_title("Network In")
axis[1, 0].set_ylabel('Bytes')

# For Network In
axis[1, 1].plot(x4,y4)
axis[1, 1].set_title("Network Out")
axis[1, 1].set_ylabel('Bytes')


plt.show()