using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColliderScript : MonoBehaviour
{

    public static bool ChangeAnim;
    GameObject bot;


    private void Start()
    {
        bot =  GameObject.Find("ybotNormal (5)");
    }
    public void OnTriggerEnter(Collider other)
    {
        if (other.name.Contains("ybot"))
        {
            RestartBot();
        }
            

    }


    public void RestartBot()
    {
        ChangeAnim = true;
        bot.transform.position = new Vector3(-20, 1.9f, 0);
        bot.transform.Rotate(0, 0, 0);
        bot.transform.eulerAngles = new Vector3(0f,90f,0f);
    }
}
