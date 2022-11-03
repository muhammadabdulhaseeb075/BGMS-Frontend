import Http from '../http';

class Endpoints {
    static basePath = '/analytics';

    static getModelsWithFields(): Promise<object | string> {
        return Http.get(`${Endpoints.basePath}/models/`);
    }

    static getModelEntries(
        modelName: string,
        payload: object,
    ): Promise<object | string> {
        const urlPath = `${Endpoints.basePath}/models/${modelName}/`;
        return Http.post(urlPath, payload);
    }

    static filterSuggestions(
        modelName: string,
        field: string
    ): Promise<object | string> {
        const urlPath = `${Endpoints.basePath}/models/${modelName}/filter-suggestion/`;
        const queries = {
            field
        };

        return Http.get(urlPath, queries);
    }

    static getAllReports(): Promise<object | string> {
        const urlPath = `${Endpoints.basePath}/reports/`;
        return Http.get(urlPath);
    }
    
    static createReport(
        payload: object
    ): Promise<object | string> {
        const urlPath = `${Endpoints.basePath}/reports/`;
        return Http.post(urlPath, payload);
    }

    static updateReport(
        id: string,
        payload: object
    ): Promise<object | string> {
        const urlPath = `${ Endpoints.basePath }/reports/${id}/`;
        return Http.put(urlPath, payload);
    }

    static getReportTemplates(): Promise<object | string> {
        const urlPath = `${Endpoints.basePath}/report-templates/`;
        return Http.get(urlPath);
    }

    static createReportTemplate(
        payload: object
    ): Promise<object | string> {
        const urlPath = `${Endpoints.basePath}/report-templates/`;
        return Http.post(urlPath, payload); 
    }

    static exportToExcel(
        id: string
    ): Promise<object | string> {
        const urlPath = `${Endpoints.basePath}/export-reports/${id}`;
        return Http.get(urlPath); 
    }
}

export default Endpoints;
