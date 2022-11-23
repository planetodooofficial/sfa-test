//function create_tr(table_id){
//            let table_body = document.getElementById(table_id),
//            first_tr = table_body.firstElementChild
//            tr_clone = first_tr.cloneNode(true);
//
//            table_body.append(tr_clone);
//
//            clean_first_tr(table_body.firstElementChild);
//            }
//
//            function clean_first_tr(firstTr){
//            let children = firstTr.children;
//
//            children = Array.isArray(children) ? children : Object.values(children);
//            children.forEach(x=>{
//            if(x !== firstTr.lastElementChild)
//            {
//            x.firstElementChild.value = '';
//            }
//            });
//            }
//
//            function remove_tr(This){
//            if(This.closest('tbody').childElementCount == 1)
//            {
//            alert("You Don't have Permission to delete This!")
//            }else{
//            This.closest('tr').remove();
//            }
//            }
//
//            <!-- js for stay detail line -->
//            function stay_create_tr(table_id){
//            let table_body = document.getElementById(table_id),
//            first_tr = table_body1.firstElementChild
//            tr_clone = first_tr.cloneNode(true);
//
//            table_body1.append(tr_clone);
//
//            stay_clean_first_tr(table_body1.firstElementChild);
//            }
//
//            function stay_clean_first_tr(firstTr){
//            let children = firstTr.children;
//
//            children = Array.isArray(children) ? children : Object.values(children);
//            children.forEach(x=>{
//            if(x !== firstTr.lastElementChild)
//            {
//            x.firstElementChild.value = '';
//            }
//            });
//            }
//
//            function stay_remove_tr(This){
//            if(This.closest('tbody').childElementCount == 1)
//            {
//            alert("You Don't have Permission to delete This!")
//            }else{
//            This.closest('tr').remove();
//            }
//            }

//this is for one to many of travel data in travel requisition
//$(document).addEventListener('click', '#add1', function() {
//    var data_line = $(this).val();
//    data = {
//        'hr_exp_id': hr_exp_id,
//        'date': rdate,
//        'from_dates': rfrom,
//        'to_dates': rto,
//        'departs_time': rdepartstime,
//        'arrives_time': rarrivetime,
//        'mode_and_class': t_modeclass,
//    }
//    $.get('/create/TravelRequisition', data, function(data) {
//        const obj = JSON.parse(data);
//        var hr_exp_id = obj.hr_exp_id
//        var date = obj.
//        if (data) {
//            document.getElementById("buyer_address1").innerHTML = '<div id="buyer_address1">' + name + ' <br/>' + street + '<br/>' + street2 + '<br/>' + zip + '&#160;' + city + '<br/>' + state_id + ' <br/>' + country_id + '<br/> <br/>' + phone + '<br/>' + email + '<br/><br/>'
//        }
//    });
//});

$(document).ready(function(){
            $('#add').click(function(){
            $('table_body').append('
            <tr id="row'+i+'">
                <td style="width:167px;">
                    <input type="date" id="t_date" name="t_date" style="width:167px;" required="1"/>
                </td>
                <td style="width:167px;">
                    <input type="date" id="t_from" name="t_from" style="width:167px;" required="1"/>
                </td>
                <td style="width:167px;">
                    <input type="time" id="t_depart_time" name="t_depart_time" style="width:167px;" required="1"/>
                </td>
                <td style="width:167px;">
                    <input type="date" id="t_to" name="t_to" style="width:167px;" required="1"/>
                </td>
                <td style="width:167px;">
                    <input type="time" id="t_arrive_time" name="t_arrive_time" style="width:167px;" required="1"/>
                </td>
                <td style="width:169px;">
                    <select id="t_mode_class" name="t_mode_class" required="1" style="width:169px;">
                        <option></option>
                        <t t-foreach="t_mode_class" t-as="tmodclas">
                            <option t-att-value="tmodclas.id">
                                <t t-esc="tmodclas.mode_class_line"/>
                            </option>
                        </t>
                    </select>
                </td>
                <td>
                    <button id="'+i'" type="button" class="btn btn-danger remove_row">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16"
                             height="16"
                             fill="currentColor" class="bi bi-trash"
                             viewBox="0 0 16 16">
                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                            <path fill-rule="evenodd"
                                  d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                        </svg>
                    </button>
                </td>
            </tr>
            ');
            });
            });
            $(document).on('click','remove_row', function(){
            var row_id = $this.attr('id');
            $('row'+row_id+'').remove();
            });