<?php
define("FLAG", "flag{????????????}");
class info
{
    var $_;
    public function __get($name)
    {
        return $this->$name;
    }
    function ______($____)
    {
        $_ = array_reverse(explode("|", $____));
        foreach ($_ as $__) {
            $___ = explode("=", $__);
            if ($___[0] === 'id')
                $this->_['id'] = $___[1];
            else if ($___[0] === 'level')
                $this->_['authLevel'] = (int) $___[1];
            else if ($___[0] === 'pw') {
                $this->_['pw'] = $___[1];
            }
        }
    }
    function _____()
    {
        return $this->_['pw'];
    }
    function ___()
    {
        return $this->_['id'];
    }
    function ____()
    {
        return $this->_['authLevel'];
    }
    public function __construct()
    {
        $this->_['id']        = "default";
        $this->_['authLevel'] = (int) 0;
        $this->_['pw']        = md5("default_passwd");
    }
    function __($a)
    {
        $_ = rand(0, getrandmax());
        $_ = md5((string) $_ . $a);
        return $_;
    }
}
$i = new info;
if (isset($_POST['id']) && isset($_POST['pw'])) {
    $__   = true;
    $___  = md5($_POST['pw']);
    $____ = $_POST['id'];
    if (($___) === "is_this_really_md5?") {
        $_____ = 1;
    } else {
        $_____ = 0;
    }
    $______          = array();
    $______['id']    = "id=" . $____;
    $______['level'] = "level=" . $_____;
    $______['pw']    = "pw=" . $i->__($___);
    $_______         = implode("|", $______);
    $i->______($_______);
    if ($i->____() === 1) {
        echo FLAG;
    }
} else {
    $__ = false;
}
?>
<html><head><title>My auth site</title></head><body><h4>Hello <?php
if ($__)
    echo ", " . $i->___();
?></h4><?php
if ($__) {
    echo "Your ID : " . $i->___() . "<br>Your Level : " . $i->____() . "<br>Your password : " . $i->_____() . "<br>";
} else {
    echo "<form method='post' action='" . $_SERVER['PHP_SELF'] . "'>ID : <input type = 'text' name='id' /><br>PW : <input type = 'password' name='pw' /><br><input type='submit' /></form>";
}
?></body></html>