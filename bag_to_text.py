import rosbag
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Print a topic")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("topic", help="Topic name")

    args = parser.parse_args()

    bag = rosbag.Bag(args.bag_file)
    for topic, msg, t in bag.read_messages(topics=[args.topic]):
        print("Stamp:", datetime.fromtimestamp(t.to_sec()).strftime('%Y-%m-%d %H:%M:%S'))
        print(msg)
        print("------------------------")
    bag.close()


if __name__ == "__main__":
    main()
