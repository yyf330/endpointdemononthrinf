namespace php Services.ToWeb
service ToWeb
{
    string pushData(1:string data),
    string insert_pid(1:string type, 2:string workId, 3:string pid)
}
