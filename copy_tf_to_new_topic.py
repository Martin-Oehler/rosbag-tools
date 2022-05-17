import rosbag
import tf2_msgs.msg
import argparse

FRAMES_TO_COPY = ["left", "left_fisheye", "right", "right_fisheye", "frontleft", "frontleft_fisheye", "frontright",
                  "frontright_fisheye", "back", "back_fisheye", "head"]


def main():
    parser = argparse.ArgumentParser(description="Copy tf messages of the given frames onto a new topic")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_bag_file", help="Output ROS bag.")
    parser.add_argument("frames", nargs='+', help="Frames to copy")
    parser.add_argument("--tf_topic", default="/tf", help="TF topic name")
    parser.add_argument("--new_topic", default="/tf_copy", help="Output topic name")

    args = parser.parse_args()
    with rosbag.Bag(args.output_bag_file, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(args.bag_file).read_messages():
            if topic == args.tf_topic:
                msg_copy = tf2_msgs.msg.TFMessage()
                for transform in msg.transforms:
                    if transform.child_frame_id in args.frames:
                        msg_copy.transforms.append(transform)
                if not len(msg_copy.transforms) == 0:
                    outbag.write(args.new_topic, msg_copy, t)
            outbag.write(topic, msg, t)


if __name__ == "__main__":
    main()
