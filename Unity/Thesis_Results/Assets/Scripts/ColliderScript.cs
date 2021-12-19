using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColliderScript : MonoBehaviour
{

    public static bool ChangeAnim;
    static GameObject bot;


    private void Start()
    {
        bot =  GameObject.Find("ybotNormal");
    }
    public void OnTriggerEnter(Collider other)
    {
        if (other.name.Contains("ybot"))
        {
            ChangeAnim = true;
        }
            

    }


    public static void RestartBot()
    {
        bot.transform.position = new Vector3(-20, 1.9f, 0);
        bot.transform.eulerAngles = new Vector3(0f,90f,0f);
    }


}
