import rosbag
import argparse


def main():
    parser = argparse.ArgumentParser(description="Splits the bag file into smaller parts.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_base_name", help="Base name of the output bag file")
    parser.add_argument("--size", type=float, default=1, help="Approximate size of each output bag file [GB]")

    args = parser.parse_args()

    with rosbag.Bag(args.bag_file) as input_bag:
        bytes_per_message = input_bag.size / input_bag.get_message_count()
        target_size_bytes = args.size * 1e+9
        messages_per_bag = target_size_bytes / bytes_per_message
        message_count = 0
        chunk = -1
        outbag = None
        for topic, msg, t in input_bag.read_messages():
            message_count += 1
            # If bag is full or not initialized, close the current and open a new one
            if outbag is None or message_count > messages_per_bag:
                if outbag is not None:
                    outbag.close()
                message_count = 0
                chunk += 1
                bag_name = args.output_base_name + f"_{chunk}.bag"
                print("Writing bag", bag_name)
                outbag = rosbag.Bag(bag_name, "w")

            outbag.write(topic, msg, t)

        outbag.close()


if __name__ == "__main__":
    main()
