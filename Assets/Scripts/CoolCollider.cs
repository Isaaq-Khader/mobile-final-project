using System.Collections.Generic;
using UnityEngine;

public class CoolCollider : MonoBehaviour
{
	public TextMesh collisionText;

	private List<UnityEngine.XR.InputDevice> trackedDevices;



	void OnTriggerEnter(Collider c)
	{
		float amplitude = 0.9f;
		float duration = 0.3f;
		collisionText.text = c.gameObject.name;
		var activated_controller = c.gameObject.name;
		
		if (activated_controller == "OVRControllerPrefab_L")
		{
			SendImpulse(amplitude, duration, "Oculus Touch Controller - Left");
		}
		else if (activated_controller == "OVRControllerPrefab_R")
		{
			SendImpulse(amplitude, duration, "Oculus Touch Controller - Right");
		}
		else if (activated_controller == "OVRPlayerController_Both")
		{
			SendImpulseBoth(amplitude, duration);
		}

	}

	void OnTriggerExit(Collider c)
	{
		collisionText.text = "Trigger Exited";
	}

	void SendImpulse(float amplitude, float duration, string activated_controller)
    {
        foreach (var device in trackedDevices)
        {
            if (device.TryGetHapticCapabilities(out var capabilities) &&
                capabilities.supportsImpulse && device.name == activated_controller)
            {
                device.SendHapticImpulse(0u, amplitude, duration);
            }
        }
    }

	void SendImpulseBoth(float amplitude, float duration)
    {
        foreach (var device in trackedDevices)
        {
            if (device.TryGetHapticCapabilities(out var capabilities) &&
                capabilities.supportsImpulse)
            {
                device.SendHapticImpulse(0u, amplitude, duration);
            }
        }
    }

	void OnCollisionEnter(Collision c)
	{
		collisionText.text = "Collided";
		
	}

	void OnCollisionExit(Collision c)
	{
		collisionText.text = "Collision exited";
	}

	void Update() 
	{
		trackedDevices = new List<UnityEngine.XR.InputDevice>();
        var desiredCharacteristics = UnityEngine.XR.InputDeviceCharacteristics.TrackedDevice;
        UnityEngine.XR.InputDevices.GetDevicesWithCharacteristics(desiredCharacteristics, trackedDevices);
	}

// 	void PlayHaptics(Collider c)
// 	{



// 		if (controller == OVRInput.Controller.LTouch)
// 			OVRHaptics.LeftChannel.Preempt(hapticsClip);
// 		else
// 			OVRHaptics.RightChannel.Preempt(hapticsClip);
// 	}

//     OVRInput.Controller controller = side == Side.Left ? OVRInput.Controller.LTouch : OVRInput.Controller.RTouch;
//     controller.SendHapticImpulse(0.5f, 0.5f, 0.5f);	
}
