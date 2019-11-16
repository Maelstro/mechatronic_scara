//#include<hFramework.h>
#include <cmath>

namespace scara {
    struct position {
        double x;
        double y;
    }

    class Robot {
        Robot(double arm1, double arm2, double height):
            arm1(arm1_),
            arm2(arm2_),
            height(height_) {
                // hMot3.setEncoderPolarity(Polarity::Reversed);  //changing encoder polarity (Polarity::Normal is default)
                // hMot3.setMotorPolarity(Polarity::Reversed);    //changing motor polarity
                // hMot3.setEncoderPolarity(Polarity::Reversed);  //changing encoder polarity (Polarity::Normal is default)
                // hMot3.setMotorPolarity(Polarity::Reversed);    //changing motor polarity
            }
        public:
            void move_to(double theta1, double theta2) {
                theta1_ = theta1;
                theta2_ = theta2;
                // hMot2.rotAbs(theta1, 200, true, INFINITE);
                // hMot3.rotAbs(theta2, 200, true, INFINITE);
            }

            void move_to(position pos) {
                double D = (pos.x*pos.x + pos.y*pos.y - arm1_*arm1_ - arm2_*arm2_)/2*arm1_*arm2_;
                theta2_ = atan(sqrt(1-D*D)/D);
                theta1_ = atan(pos.y/pos.x) - atan((arm2_*sin(theta2_))/(arm1_+arm2_*cos(theta2_)));
                // hMot2.rotAbs(theta1_, 200, true, INFINITE);
                // hMot3.rotAbs(theta2_, 200, true, INFINITE);
            }
            
            void move_by(position pos) {
                auto current_pos = get_pos();
                move_to(current_pos.x + pos.x, current_pos.y + pos.y);
            }

            position get_pos() {
                position pos;
                pos.x = arm1_*cos(theta1_)+arm2_*cos(theta1_+theta2_);
                pos.y = arm1_*sin(theta1_)+arm2_*sin(theta1_+theta2_);
            }

            void pen_up(bool up);

        protected:
            double arm1_, arm2_, height_;
            double theta1_;
            double theta2_;
    };
}