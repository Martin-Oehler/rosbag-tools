#!/usr/bin/env python3
import rosbag
import argparse
import os

from typing import List
from pytransform3d import transformations as pt
from src.transform_conversions import transform_msg_to_np, transform_np_to_msg


def parse_args():
    parser = argparse.ArgumentParser(description="Change the names of tf frames or invert the transform.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("remappings", nargs="+", help="A list of tf frame remappings (old:=new) or transform inversions (parent!child)")

    return parser.parse_args()


def read_mapping(remap_list: List[str]):
    mappings = dict()
    inversions = dict()
    for remap in remap_list:
        parts = remap.split(":=")
        if len(parts) == 2:
            mappings[parts[0]] = parts[1]
        parts = remap.split("!")
        if len(parts) == 2:
            inversions[parts[0]] = parts[1]
    return mappings, inversions

def invert_transform(transform_msg):
    child = transform_msg.child_frame_id
    transform_msg.child_frame_id = transform_msg.header.frame_id
    transform_msg.header.frame_id = child

    transform = transform_msg_to_np(transform_msg.transform)
    transform_inv = pt.invert_transform(transform)
    transform_msg.transform = transform_np_to_msg(transform_inv)


def remap_tf(bag_in: rosbag.Bag, bag_out: rosbag.Bag, remappings, inversions):
    tf_topics = ["/tf", "/tf_static"]
    for topic, msg, t, header in bag_in.read_messages(return_connection_header=True):
        if topic in tf_topics:
            for transform in msg.transforms:
                if transform.child_frame_id in remappings:
                    transform.child_frame_id = remappings[transform.child_frame_id]
                if transform.header.frame_id in remappings:
                    transform.header.frame_id = remappings[transform.header.frame_id]

                if transform.header.frame_id in inversions and inversions[transform.header.frame_id] == transform.child_frame_id:
                    invert_transform(transform)
            bag_out.write(topic, msg, t, connection_header=header)
        else:
            bag_out.write(topic, msg, t, connection_header=header)


def main():
    args = parse_args()
    remappings, inversions = read_mapping(args.remappings)

    bag_file_path_parts = os.path.splitext(args.bag_file)
    if len(bag_file_path_parts) != 2:
        print("Malformed bag_path", args.bag_file)
        return
    output_bag_file = bag_file_path_parts[0] + "_tf_remap" + bag_file_path_parts[1]

    with rosbag.Bag(output_bag_file, 'w') as bag_out, rosbag.Bag(args.bag_file) as bag_in:
        remap_tf(bag_in, bag_out, remappings, inversions)


if __name__ == "__main__":
    main()
