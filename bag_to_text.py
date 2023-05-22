import rosbag
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Print a topic")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("topic", help="Topic name")
    parser.add_argument('--compact', action='store_true', help="Merge entries with identical message")

    args = parser.parse_args()

    bag = rosbag.Bag(args.bag_file)
    previous_msg = None
    for topic, msg, t in bag.read_messages(topics=[args.topic]):
        if not args.compact or previous_msg is None or previous_msg != msg:
            print("------------------------")
            print(msg)
        previous_msg = msg
        print("Stamp:", datetime.fromtimestamp(t.to_sec()).strftime('%Y-%m-%d %H:%M:%S'))
    bag.close()


if __name__ == "__main__":
    main()
