<?php
error_reporting(E_ERROR | E_PARSE);
session_start();
if(isset($_SESSION['level'])){
	$level=$_SESSION['level'];
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<!DOCTYPE html>
<html lang="en">
<head>
  <title>admin view</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1"> 
   <script src="bootstrap/js/jquery-1.11.2.min.js"></script>  
	<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.min.css">			
	<link rel="stylesheet" type="text/css" href="css/css.css">
	<link rel="stylesheet" type="text/css" href="css/slidecss.css">
    <script type="text/javaScript" src="bootstrap/js/bootstrap.min.js"></script>
    <script type="text/javaScript">
    $(document).ready(function(){
    	$("#showdocuments").click(function(){
    		$("#documents").toggle(1000);
    	});
    });
   function validatestaffid(){
	var staffid =document.search.staffid.value;
	if(staffid==""){
	  	produceprompt("PLEASE ENTER STAFF ID NUMBER","prompt","red");
		return false;
	  }
	  if(/[^0-9a-bA-B\s]/gi.test(staffid)){
		produceprompt("THIS IS INVALID STAFF ID NUMBER ","prompt","red");
		return false;
	}else{
		produceprompt("good","prompt","green");
		return true;
	}
}
function produceprompt(message, promptlocation, color){
	document.getElementById(promptlocation).innerHTML = message;
	document.getElementById(promptlocation).style.color = color;
}


</script>	
</head>
<body>

<div class="container" id="wrapper">

<nav class="navbar navbar-inverse" role="navigation">  
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>                        
      </button>      
    </div>
    <div class="collapse navbar-collapse" id="myNavbar">
      <ul class="nav navbar-nav">
             
        <?php
        if($level=='Administrator'){
        	echo "<li><a href='addstaff.php'>CREAT NEW USER ACCOUNT</a></li>";  
        }

         ?>      
      </ul> 
        
      <button class="btn btn-primary" onclick="history.go(-1)">BACK</button>  
    </div>
    </nav>   
<div class="container borders">			
				<div class="col-lg-12 "id="searcharea" >
				<form class="form-inline" name="search" method="POST" action="records.php">			
					<label class="input-lg">STAFF ID NUMBER</label>					
		   			<input type="text" size="1" class="input-lg" value="<?php if(isset($_POST['staffid'])) echo $_POST['staffid'];?>" name="staffid"  required><label id="prompt"></label>
                       <label class="input-lg">FIRST DATE</label>
                    <input type="date" size="3" class="input-lg" value="<?php if(isset($_POST['first_date'])) echo $_POST['first_date'];?>" name="first_date"  required><label id="prompt"></label>
                    <label class="input-lg">LAST DATE</label>
                    <input type="date" size="3" class="input-lg" value="<?php if(isset($_POST['last_date'])) echo $_POST['last_date'];?>" name="last_date"  required><label id="prompt"></label>													
					<button class="btn btn-primary btn-md" type="submit" name="search">SEARCH</button>				
				</form>					         
	 			</div><!--search area-->
	   <div class="col-lg-12" id="display">
	   	   <?php
	   	   require 'database/connection.php';
	      if(isset($_POST['search'])){
           $staffid = $_POST['staffid'];
           $first_date = $_POST['first_date'];
           $last_date = $_POST['last_date'];
	       if(!empty($staffid) && !empty($first_date) && !empty($last_date)){
	       	$sql=mysqli_query($dbc,"SELECT * FROM time_out WHERE staffid='$staffid' and date BETWEEN '$first_date' AND '$last_date'");
	       	if(mysqli_num_rows($sql)>0){
	       		while ($row=mysqli_fetch_array($sql)){
	       			$staffid= $row['staffid'];
	       			$time_in = $row['time_out'];
	       			$date = $row['date'];
	       			$output = '<table class="table table-stripped" id="filtertable2">
                       
                           <tr>
                               <td><label>STAFF ID</label></td>
                               <td><input type="text" readonly value='.$staffid.' ></td>
                               <td><label>TIME IN</label></td>
                             <td><input type="text" readonly value='.$time_out.' ></td>
                             <td><label>DATE</label></td>
                               <td><input type="text" readonly value='.$date.' ></td>
                           </tr>
                       
                               
                           
                             
                       </table>';
                    echo $output;

	       		}//while array    
        
	     
	       	}else{
	       		echo "<div class='alert alert-warning'>
	 				 <a href='#' class='close' data-dismiss='alert'>&times;</a>
	 				<strong>Error!</strong> THIS INPUTS DIDN'T MATCH ANY RECORDS.
	 				 </div>";	       
	       }
	   }
 }//isset
	      ?>
	     
	   </div><!--display-->
 </div><!-- content container-->

</div><!--end wrapper container-->
<!--importing login_modal-->
</body>
</html>





