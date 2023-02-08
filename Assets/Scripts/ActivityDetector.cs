using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.UI;

public class ActivityDetector : MonoBehaviour
{
    // Feel free to add additional class variables here
    OculusSensorReader sensorReader;
    private Text textBox;
    private List<Dictionary<string, Vector3>> attr_array = new List<Dictionary<string, Vector3>>();

    // Start is called before the first frame update
    void Start()
    {
        sensorReader = new OculusSensorReader();
        textBox = this.GetComponent<Text>();
    }

    /// <summary>
    /// Return the activity code of the current activity. Feel free to add
    /// additional parameters to this function.
    /// </summary>
    string GetCurrentActivity(Dictionary<string, Vector3> attributes)
    {
        if (attr_array.Count < 180)
        {
            attr_array.Add(attributes);
        }
        else
        {
            // get mean and var for calculations
            mean = attr_array.Average();
            var = attr_array.Var();
            attr_array.RemoveAt(0);
            attr_array.Add(attributes);
        }
        // left and right velocites for sit/stand diff and overhead vel
        var left_controller_vel = var["controller_left_vel"];
        var right_controller_vel = var["controller_right_vel"];

        var headset_ang_vel = var["headset_angularVel"].y;

        var left_controller_ang_vel = mean["controller_left_angularVel"].y;
        var right_controller_ang_vel = mean["controller_right_angularVel"].y;

        var headset_vel = var["headset_vel"].y;

        // TODO: Implement your algorithm here to determine the current activity based
        // on recent sensor traces.
        if (Math.Abs(headset_ang_vel - 0.02513) < 0.565 || headset_ang_vel > 0.02513)
        {
            return "Twisting";
        }
        if ((left_controller_vel.x < 0.01 && left_controller_vel.y < 0.01 && left_controller_vel.z < 0.01) &&
            (right_controller_vel.x < 0.01 && right_controller_vel.y < 0.01 && right_controller_vel.z < 0.01))
        {
            sit_l_controller_to_headset_position = Math.Abs(0.14958 + 0.57612);
            sit_r_controller_to_headset_position = Math.Abs(0.14958 + 0.57648);

            if (Math.Abs(sit_l_controller_to_headset_position - Math.Abs(mean["headset_pos"].y - mean["controller_left_pos"].y)) < 0.25 
                && Math.Abs(sit_r_controller_to_headset_position - Math.Abs(mean["headset_pos"].y - mean["controller_right_pos"].y)) < 0.25)
            {
                return "Sitting";
            }
            else
            {
                return "Standing";
            }
        }
        if (Math.Abs(0.154219 - var["headset_vel"].y) < 0.15)
        {
            return "Jogging";
        }
        if ((Math.Abs(0.71396 - left_controller_vel.y) < 0.5)
            && (Math.Abs(0.6995 - right_controller_vel.y) < 0.5))
        {
            return "Overhead";
        }
        if ((Math.Abs(0.06568 - left_controller_ang_vel) < 0.15)
            && (Math.Abs(-0.08513 - right_controller_ang_vel) < 0.15))
        {
            return "Stretching";
        }

        return "Unknown"; // otherwise we are unsure of what activity the user is doing
    }

    // Update is called once per frame
    void Update()
    {
        sensorReader.RefreshTrackedDevices();

        // Fetch attributes as a dictionary, with <device>_<measure> as a key
        // and Vector3 objects as values
        var attributes = sensorReader.GetSensorReadings();

        var currentActivity = GetCurrentActivity(attributes);
        
        // TODO: Update the Activity Sign text based on the detected activity
        textBox.text = "Activity: " + currentActivity;
    }
}
