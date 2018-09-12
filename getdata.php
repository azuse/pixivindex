<?php
header("Access-Control-Allow-Origin: *");
$dbhost = 'localhost:3306';  // mysql服务器主机地址
$dbuser = 'root';            // mysql用户名
$dbpass = 'misakaxindex';          // mysql用户名密码
$conn = mysqli_connect($dbhost, $dbuser, $dbpass);
if(! $conn )
{
    die('连接失败: ' . mysqli_error($conn));
}
// 设置编码，防止中文乱码
mysqli_query($conn , "set names utf8");
 
$sql = 'SELECT * FROM `picindex` ORDER BY cast(createtime as datetime) DESC';
 
mysqli_select_db( $conn, 'pixiv' );
$retval = mysqli_query( $conn, $sql );
if(! $retval )
{
    die('无法读取数据: ' . mysqli_error($conn));
}
global $dataBuf;
$i=0;
while($row = mysqli_fetch_assoc($retval))
{
    $temp["state"] = $row['state'];
    $temp["filename"] = $row['filename'];
    $temp["tag"] = $row['tag'];
    $temp["sourceurl"] = $row['sourceurl'];
    $temp["author"] = $row['author'];
    $temp["picpageurl"] = $row['picpageurl'];
    $temp["character"] = $row['character'];
    $dataBuf[$i++] = $temp;
}
echo json_encode($dataBuf); 
mysqli_close($conn);
?>