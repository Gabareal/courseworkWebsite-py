// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-analytics.js";
import { getDatabase,get,ref,child,set,onValue } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";
import { getAuth,signInWithEmailAndPassword } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js';

const submit = document.getElementById('submit'), 
user_email = document.getElementById("user_email"), 
user_password = document.getElementById('user_password');

const firebaseConfig = {
  apiKey: "AIzaSyBBKv0bFftovEPZhZ_k2XbjrEoATf68O1A",
  authDomain: "coursework-7e5bd.firebaseapp.com",
  databaseURL: "https://coursework-7e5bd-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "coursework-7e5bd",
  storageBucket: "coursework-7e5bd.appspot.com",
  messagingSenderId: "627904949119",
  appId: "1:627904949119:web:72cccf95f57b94f30ac84a",
  measurementId: "G-BL42H0QM79"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getDatabase();
const dbref = ref(db);

function getUserPerms(userId) {
    console.log(userId)
    const reference = ref(db, 'users/' + userId);
    return get(reference)
      .then((snapshot) => {
        if (snapshot.exists()) {
            console.log(snapshot.val().permissions)
          return snapshot.val().permissions;
        } else {
          console.error('User data not found');
          return null;
        }
      })
      .catch((error) => {
        console.error('Error getting user permissions:', error);
        return null;
      });
  }


submit.onclick = e => {
    signInWithEmailAndPassword(auth, user_email.value, user_password.value)
    .then((credentials)=>{
        get(child(dbref,'UsersAuthList/'+ credentials.user.uid)).then((snapshot)=>{
            if (snapshot.exists){
                sessionStorage.setItem("user-info", JSON.stringify({userEmail: user_email.value}))
                sessionStorage.setItem("user-creds", JSON.stringify(credentials.user));
                getUserPerms(credentials.user.uid).then((permissions)=> {
                    sessionStorage.setItem("user-perms", JSON.stringify(permissions));
                    window.location.href = "protected"
                })
            }
        })
    })
    .catch((error)=>{
        alert(error.message);
        console.log(error.code);
        console.log(error.message)
    })
}
