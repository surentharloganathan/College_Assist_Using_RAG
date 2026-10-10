package com.surenthar.rag.service;

import com.surenthar.rag.client.RagApiClient;
import com.surenthar.rag.dto.AnswerResponse;
import com.surenthar.rag.dto.QuestionRequest;
import org.springframework.stereotype.Service;

@Service
public class RagService {

    private final RagApiClient ragApiClient;

    public RagService(RagApiClient ragApiClient) {
        this.ragApiClient = ragApiClient;
    }

    public AnswerResponse processanswer(QuestionRequest request) {

        return ragApiClient.askQuestion(request);
    }
}