using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimatorController : MonoBehaviour
{
    Animator animator;
    // Start is called before the first frame update
    void Start()
    {
        Animator animator;
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey("w")){
            animator.SetBool("First",true);
        }
    }
}
