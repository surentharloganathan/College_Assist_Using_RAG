package com.surenthar.rag.client;

import com.surenthar.rag.dto.AnswerResponse;
import com.surenthar.rag.dto.QuestionRequest;
import org.jspecify.annotations.NonNull;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class RagApiClient {

    private final RestClient restClient;

    public RagApiClient(
            RestClient.@NonNull Builder restClientBuilder,
            @Value("${rag.api.base-url}") String baseUrl) {

        this.restClient = restClientBuilder
                .baseUrl(baseUrl)
                .build();
    }

    public AnswerResponse askQuestion(QuestionRequest request) {

        return restClient.post()
                .uri("/ask")
                .body(request)
                .retrieve()
                .body(AnswerResponse.class);
    }
}