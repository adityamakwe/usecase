import { Component, OnInit } from "@angular/core";
import { ServiceLocatorService } from "./service-locator.service";
import { ActivatedRoute } from "@angular/router";


@Component({
    template: ''
})
export class BaseCtl implements OnInit {

    public form: any = {
        error: false, //error 
        inputerror: {}, // form input error messages
        message: null, //error or success message
        data: { id: 0 }, //form data
        searchParams: {}, //search form
        preload: [], // preload data
        list: [], // search list 
        nextListSize: 0,
        pageNo: 0
    };

    public api: any = {
        endpoint: '',
        get: '',
        save: '',
        search: '',
        delete: '',
        preload: '',
    }

    initApi(ep: any) {
        this.api.endpoint = ep;
        this.api.get = ep + "/get";
        this.api.save = ep + "/save";
        this.api.search = ep + "/search";
        this.api.delete = ep + "/delete";
        this.api.preload = ep + "/preload";
    }

    constructor(public endpoint: String, public serviceLocator: ServiceLocatorService, public route: ActivatedRoute) {
        var _self = this;
        _self.initApi(endpoint); // http://localhost:8000/orsapi/Doctor

        serviceLocator.getPathVariable(route, function (params: any) {
            // _self.form.data.id = params["id"];
            const id = params["id"];
            _self.form.data.id = id && !isNaN(id) ? Number(id) : 0;   
        })
    }


    ngOnInit(): void {
        this.preload();
        if (this.form.data.id && this.form.data.id > 0) {
            this.display();
        }
    }

    display() {
        var _self = this;
        this.serviceLocator.httpService.get(_self.api.get + "/" + _self.form.data.id, function (res: any) {
            if (res.success) {
                _self.form.data = res.result.data;
            } else {
                _self.form.error = true;
                _self.form.message = res.result.message;
            }
        });
    }

    preload() {
        var _self = this;
        this.serviceLocator.httpService.get(_self.api.preload, function (res: any) {
            if (res.success) {
                _self.form.preload = res.result;
            } else {
                _self.form.error = true;
                _self.form.message = res.result.message;
            }
        });
    }

    // submit() {
    //     var _self = this;
    //     this.serviceLocator.httpService.post(this.api.save, this.form.data, function (res: any) {
    //         _self.form.message = '';
    //         _self.form.inputerror = {};
    //         if (res.success) {
    //             _self.form.message = res.result.message;
    //             _self.form.data.id = res.result.data;
    //         } else {
    //             _self.form.error = true;
    //             if (res.result.inputerror) {
    //                 _self.form.inputerror = res.result.inputerror;
    //             }
    //             _self.form.message = res.result.message;
    //         }
    //     });
    // }

    submit() {
        var _self = this;

        // 🔥 Force numeric id before sending to backend
        if (!_self.form.data.id || isNaN(_self.form.data.id)) {
            _self.form.data.id = 0;
        }

        this.serviceLocator.httpService.post(this.api.save, this.form.data, function (res: any) {
            _self.form.message = '';
            _self.form.inputerror = {};

            if (res.success) {
                _self.form.error = false;
                _self.form.message = res.result.message;

                if (res.id) {                 // Django sends id
                    _self.form.data.id = res.id;
                }
            } else {
                _self.form.error = true;
                if (res.result.inputerror) {
                    _self.form.inputerror = res.result.inputerror;
                }
                _self.form.message = res.result.message;
            }
        });
    }


    search() {
        var _self = this;
        console.log("Calling API with pageNo ===============", this.form.pageNo);

        this.serviceLocator.httpService.post(_self.api.search, _self.form, function (res: any) {
            _self.form.message = '';
            _self.form.list = [];
            if (res.success) {
                _self.form.error = false;
                _self.form.list = res.result.data;
                _self.form.nextListSize = res.result.nextListSize;
            } else {
                _self.form.error = true;
                _self.form.message = res.result.message;
            }
        });
    }

    reset() {
        location.reload();
    }

    delete(id: any) {
        var _self = this;
        this.serviceLocator.httpService.post(_self.api.delete + "/" + id, this.form, function (res: any) {
            _self.form.message = '';
            _self.form.list = [];
            if (res.success) {
                _self.form.error = false;
                _self.form.message = res.result.message;
                _self.form.list = res.result.data;
            } else {
                _self.form.error = true;
                _self.form.message = res.result.message;
            }
        });

    }
    forward(page: any) {
        this.serviceLocator.forward(page);
    }
}