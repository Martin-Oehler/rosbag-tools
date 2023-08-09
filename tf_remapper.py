import rosbag
import argparse
import os

from typing import List


def parse_args():
    parser = argparse.ArgumentParser(description="Print a topic")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("remappings", nargs="+", help="A list of tf frame remappings in the form of 'old:=new'")

    return parser.parse_args()


def read_remappings(remap_list: List[str]):
    remappings = dict()
    for remap in remap_list:
        parts = remap.split(":=")
        if len(parts) != 2:
            print("Malformed remapping:", remap)
            continue
        remappings[parts[0]] = parts[1]
    return remappings


def remap_tf(bag_in, bag_out, remappings):
    tf_topics = ["/tf", "/tf_static"]
    for topic, msg, t in bag_in.read_messages():
        if topic in tf_topics:
            for transform in msg.transforms:
                if transform.child_frame_id in remappings:
                    transform.child_frame_id = remappings[transform.child_frame_id]
                if transform.header.frame_id in remappings:
                    transform.header.frame_id = remappings[transform.header.frame_id]
            bag_out.write(topic, msg, t)
        else:
            bag_out.write(topic, msg, t)


def main():
    args = parse_args()
    remappings = read_remappings(args.remappings)

    bag_file_path_parts = os.path.splitext(args.bag_file)
    if len(bag_file_path_parts) != 2:
        print("Malformed bag_path", args.bag_file)
        return
    output_bag_file = bag_file_path_parts[0] + "_tf_remap" + bag_file_path_parts[1]

    with rosbag.Bag(output_bag_file, 'w') as bag_out, rosbag.Bag(args.bag_file) as bag_in:
        remap_tf(bag_in, bag_out, remappings)


if __name__ == "__main__":
    main()
