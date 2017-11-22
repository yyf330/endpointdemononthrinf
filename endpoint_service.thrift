
service endpointControl{
        i32 create_capture_p(1:i32 workid,2:string s_name,3:i32 cid),
        i32 create_trnsp_p(1:i32 workid,2:string s_name,3:i32 cid),
        i32 create_load_p(1:i32 workid,2:string s_name,3:i32 cid),
        i32 start_p(1:string s_name),
        i32 stop_p(1:string s_name),
        i32 del_p(1:string s_name),
        string get_ip()
}
