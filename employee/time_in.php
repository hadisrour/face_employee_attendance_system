<?php
require 'database/connection.php';
if(isset($_POST['time_in'])){
	
	$staffid = $_POST['staffid'];
	
	$time_in = $_POST['time_in'];
	$date = $_POST['date'];

if(isset($staffid) && isset($time_in) && isset($date)){

if(!empty($staffid) && !empty($time_in) && !empty($date)){

	$insertsql=mysqli_query($dbc,"INSERT INTO time_in (staffid, time_in, date) 
		VALUES('".$staffid." ','".$time_in."','".$date."')"); 

	if($insertsql){
		$_SESSION['saved'] = "<div class='alert alert-success'>
	 				 <a href='#' class='close' data-dismiss='alert'>&times;</a>
	 				  <strong>Success!</strong><h3>TIME_IN FORM REGISTERED SUCCESSFULLY</h3>
	 				 </div>";	 				 
	 				 header('location:index.php'); 
	}else{
		$saveerror= "<div class='alert alert-warning'>
	 				 <a href='#' class='close' data-dismiss='alert'>&times;</a>
	 				  <strong>alert!</strong><h3>A PROBLEM HAS OCCURED. PLEASE TRY AGAIN... </h3>
	 				 </div>"; 
	}

}else{
	$exist= "<div class='alert alert-warning'>
	 				 <a href='#' class='close' data-dismiss='alert'>&times;</a>
	 				<strong>Error!</strong> THIS TIME_IN FORM HAS NOT BEEN REGISTERED.
	 				 </div>";
}

	
}else{
	$emptyfields ="<div class='alert alert-warning'>
	 				<a href='#' class='close' data-dismiss='alert'>&times;</a>
	 				<strong>Error!</strong> PLEASE FILL ALL THE REQUIRED FILEDS.
	 				 </div>";
}

}



?>
<script src="bootstrap/js/jquery-1.11.2.min.js"></script>
<link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.min.css">			
	<link rel="stylesheet" type="text/css" href="css/css.css">
	<link rel="stylesheet" type="text/css" href="css/slidecss.css">
    <script type="text/javaScript" src="bootstrap/js/bootstrap.min.js"></script>
<script type="text/javaScript">
    


    function validatestaffid(){
	var staffid =document.register.staffid.value;
	if(staffid==""){
	  	produceprompt("PLEASE ENTER STAFF ID NUMBER","staffidprompt","red");
		return false;
	  }
	  if(/[^0-9a-bA-B\s]/gi.test(staffid)){
		produceprompt("INVALID STAFF ID NUMBER ","staffidprompt","red");
		return false;
	}else{
		produceprompt("good","staffidprompt","green");
		return true;
	}
}
 
function produceprompt(message, promptlocation, color){
	document.getElementById(promptlocation).innerHTML = message;
	document.getElementById(promptlocation).style.color = color;
}

</script>
<div class="" id="register">
	<div class="modal-dialog">
		<div class="modal-content">		
			<div class="modal-header">			
				<h3>TIME_IN FORM</h3>
				<button class="btn btn-primary" onclick="history.go(-1);">BACK</button>
				<?php if(isset($saved))echo $saved;?>
				<?php if(isset($saveerror))echo $saveerror;?>
				<?php if(isset($exist))echo $exist;?>
				<?php if(isset($passwordmismatch))echo $passwordmismatch;?>
				<?php if(isset($emptyfields)) echo $emptyfields;?>
			</div><!--modal-header-->
			<div class="modal-body">
			<form class="form-horizontal" action="time_in.php" method="POST" name="register">

				<div class="form-group">

				<div class="form-group">
				<label for="staffid" class="col-lg-4 control-label">STAFF ID NUMBER</label>
				<div class="col-lg-8">
					<input type="text" class="form-control" name="staffid" value="<?php if(isset($staffid))echo $staffid;?>" placeholder="ENTER STAFF ID NUMBER">
				</div>
				</div><!--form-group-->


				<div class="form-group">
				<label for="staffid" class="col-lg-4 control-label">TIME_IN</label>
				<div class="col-lg-8">
					<input type="text" class="form-control" name="time_in" value="<?php if(isset($time_in))echo $time_in;?>" placeholder="ENTER TIME_IN">
				</div>
				</div><!--form-group-->

				<div class="form-group">
				<label for="staffid" class="col-lg-4 control-label">DATE</label>
				<div class="col-lg-8">
					<input type="text" class="form-control" name="date" value="<?php if(isset($date))echo $date;?>" placeholder="ENTER DATE">
				</div>
				</div><!--form-group-->
	
				<div class="form-group">
				<div class="col-sm-4 col-lg-offset-4">
					<button class="btn btn-primary form-control" type="submit" name="register">SAVE</button>
				</div>							
				</div><!--form-group-->
				</form>	
				
			</div><!--modal-body-->
			<div class="modal-footer">				
				<p></p>
			</div><!--modal-footer-->			
		</div><!--modal-content-->
	</div><!--modal-dialog-->
</div><!--modal-starting-->