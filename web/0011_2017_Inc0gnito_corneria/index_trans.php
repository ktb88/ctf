<?php
define("FLAG", "flag{????????????}");
class info
{
    var $m_info;
    public function __get($name)
    {
        return $this->$name;
    }
    function parse_args($arg)
    {
        $explode_arr = array_reverse(explode("|", $arg));
        foreach ($explode_arr as $kv) {
            $arr_kv = explode("=", $kv);
            if ($arr_kv[0] === 'id')
                $this->m_info['id'] = $arr_kv[1];
            else if ($arr_kv[0] === 'level')
                $this->m_info['authLevel'] = (int) $arr_kv[1];
            else if ($arr_kv[0] === 'pw') {
                $this->m_info['pw'] = $arr_kv[1];
            }
        }
    }
    function get_pw()
    {
        return $this->m_info['pw'];
    }
    function get_id()
    {
        return $this->m_info['id'];
    }
    function get_level()
    {
        return $this->m_info['authLevel'];
    }
    public function __construct()
    {
        $this->m_info['id']        = "default";
        $this->m_info['authLevel'] = (int) 0;
        $this->m_info['pw']        = md5("default_passwd");
    }
    function ret_rnd($a)
    {
        $_ = rand(0, getrandmax());
        $_ = md5((string) $_ . $a);
        return $_;
    }
}
$i = new info;
if (isset($_POST['id']) && isset($_POST['pw'])) {
    $ret   = true;
    $pw_md5  = md5($_POST['pw']);
    $id = $_POST['id'];
    if (($pw_md5) === "is_this_really_md5?") {
        $level = 1;
    } else {
        $level = 0;
    }
    $new_arr          = array();
    $new_arr['id']    = "id=" . $id;
    $new_arr['level'] = "level=" . $level;
    $new_arr['pw']    = "pw=" . $i->ret_rnd($pw_md5);
    $imp_arr         = implode("|", $new_arr);
    $i->parse_args($imp_arr);
    if ($i->get_level() === 1) {
        echo FLAG;
    }
} else {
    $ret = false;
}
?>
<html><head><title>My auth site</title></head><body><h4>Hello <?php
if ($ret)
    echo ", " . $i->get_id();
?></h4><?php
if ($ret) {
    echo "Your ID : " . $i->get_id() . "<br>Your Level : " . $i->get_level() . "<br>Your password : " . $i->get_pw() . "<br>";
} else {
    echo "<form method='post' action='" . $_SERVER['PHP_SELF'] . "'>ID : <input type = 'text' name='id' /><br>PW : <input type = 'password' name='pw' /><br><input type='submit' /></form>";
}
?></body></html>