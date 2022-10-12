#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/exact_time.h>
#include <sensor_msgs/Image.h>
#include <darknet_ros_msgs/BoundingBox.h>
#include <darknet_ros_msgs/BoundingBoxes.h>

using namespace sensor_msgs;
using namespace darknet_ros_msgs;
using namespace message_filters;

void callback(const ImageConstPtr& img_msg, const BoundingBoxesConstPtr& box_msg)
{
  // Solve all of perception here...
}

int main(int argc, char** argv)
{
  ros::init(argc, argv, "vision_node");

  ros::NodeHandle nh;
  message_filters::Subscriber<Image> img_sub(nh, "/darknet_ros/detection_image", 1);
  message_filters::Subscriber<BoundingBoxes> box_sub(nh, '/darknet_ros/bounding_boxes', 1);

  typedef sync_policies::ExactTime<Image, BoundingBoxes> MySyncPolicy;
  // ExactTime takes a queue size as its constructor argument, hence MySyncPolicy(10)
  Synchronizer<MySyncPolicy> sync(MySyncPolicy(10), img_sub, box_sub);
  sync.registerCallback(boost::bind(&callback, _1, _2));

  ros::spin();

  return 0;
}
