from pytransform3d import transformations as pt
import numpy as np
import geometry_msgs.msg

def transform_msg_to_np(transform_msg):
    pq = np.array([transform_msg.translation.x,
                   transform_msg.translation.y,
                   transform_msg.translation.z,
                   transform_msg.rotation.w,
                   transform_msg.rotation.x,
                   transform_msg.rotation.y,
                   transform_msg.rotation.z])
    return pt.transform_from_pq(pq)

def transform_np_to_msg(transform):
    transform_msg = geometry_msgs.msg.Transform()
    pq = pt.pq_from_transform(transform)
    transform_msg.translation.x = pq[0]
    transform_msg.translation.y = pq[1]
    transform_msg.translation.z = pq[2]
    transform_msg.rotation.w = pq[3]
    transform_msg.rotation.x = pq[4]
    transform_msg.rotation.y = pq[5]
    transform_msg.rotation.z = pq[6]
    return transform_msg