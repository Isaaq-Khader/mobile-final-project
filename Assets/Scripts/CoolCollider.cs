using System.Collections.Generic;
using UnityEngine;

public class CoolCollider : MonoBehaviour
{
	public OVRInput.Controller controller;

	public TextMesh collisionText;

	private List<UnityEngine.XR.InputDevice> trackedDevices;



	void OnTriggerEnter(Collider c)
	{
		SendImpulse(0.5f, 0.1f);
		collisionText.text = "Trigger Entered";
	}

	void OnTriggerExit(Collider c)
	{
		collisionText.text = "Trigger Exited";
	}


	void SendImpulse(float amplitude, float duration)
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
