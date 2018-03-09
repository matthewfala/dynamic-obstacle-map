using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class ObjectCreator : MonoBehaviour {

	int frameCount;
	int objectCount;

	int currentFrameNum;

	GameData[] gameDatas;
	GameObject[] gameObjects;

	// Use this for initialization
	void Start () {
		objectCount = 10; // should read from configuration file later on
		frameCount = 100; // same for this one

		currentFrameNum = 0;
		gameDatas = new GameData[frameCount];
		gameObjects = new GameObject[objectCount];

		for (int i = 0; i < frameCount; i++) {
			string fileName = string.Format ("{0:D6}.json", i);
			string filePath = Path.Combine (Application.streamingAssetsPath, fileName);
			Debug.Log (filePath);
			if (File.Exists (filePath)) {
				string dataAsJson = File.ReadAllText (filePath);
				gameDatas [i] = JsonUtility.FromJson<GameData> (dataAsJson);
			}
		}

		foreach (BasicObject obj in gameDatas[currentFrameNum].objects) {
			PrimitiveType type = PrimitiveType.Cube;
			switch (obj.type) {
			case 0:
				type = PrimitiveType.Cube;
				break;
			case 1:
				type = PrimitiveType.Sphere;
				break;
			case 2:
				type = PrimitiveType.Cylinder;
				break;
			}
			gameObjects[obj.id] = GameObject.CreatePrimitive (type);
			gameObjects[obj.id].transform.position = obj.position;
			gameObjects[obj.id].transform.eulerAngles = obj.orientation;
		}

//			objs = loadedData.objects;
//			for (int i = 0; i < objs.Length; i++) {
//				Debug.Log ("object N.O.: " + i);
//				Debug.Log ("id: " + objs [i].id);
//				Debug.Log ("type: " + objs [i].type);
//				Debug.Log ("position: " + objs [i].position);
//				Debug.Log ("orientation: " + objs [i].orientation);
//				Debug.Log ("linear_velocity: " + objs [i].linear_velocity);
//				Debug.Log ("angular_velocity: " + objs [i].angular_velocity);
//				Debug.Log ("linear_acceleration: " + objs [i].linear_acceleration);
//				Debug.Log ("angular_acceleration: " + objs [i].angular_acceleration);
//
//				PrimitiveType type = PrimitiveType.Cube;
//				switch (objs [i].type) {
//				case 0:
//					type = PrimitiveType.Cube;
//					break;
//				case 1:
//					type = PrimitiveType.Sphere;
//					break;
//				}
//
//				GameObject instance = GameObject.CreatePrimitive (type);
//				instance.transform.position = objs [i].position;
//				instance.transform.eulerAngles = objs [i].orientation;
//
//			}
	}

	void Update () {
		if (currentFrameNum < frameCount) {
			currentFrameNum++;
		} else {
			currentFrameNum = 0;
		}

		foreach (BasicObject obj in gameDatas[currentFrameNum].objects) {
			gameObjects[obj.id].transform.position = obj.position;
			gameObjects[obj.id].transform.eulerAngles = obj.orientation;
		}

	}
	
}
